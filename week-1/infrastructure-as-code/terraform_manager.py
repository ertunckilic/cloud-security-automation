#!/usr/bin/env python3
"""
Day 4: Terraform state and infrastructure management using Boto3
Learn: Manage Terraform state files in S3 and monitor infrastructure
UPDATED: Fixed exception handling for bucket encryption and public access block
"""

import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime

class TerraformManager:
    """Manage Terraform state and infrastructure with improved error handling"""
    
    def __init__(self, region='us-east-1', state_bucket=None):
        self.s3_client = boto3.client('s3', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.state_bucket = state_bucket
    
    def list_state_files(self):
        """List Terraform state files in S3"""
        if not self.state_bucket:
            print("❌ State bucket not configured")
            return None
        
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.state_bucket)
            objects = response.get('Contents', [])
            
            print("\n" + "="*80)
            print("TERRAFORM STATE FILES".center(80))
            print("="*80 + "\n")
            
            if not objects:
                print("❌ No state files found")
            else:
                print(f"✅ Found {len(objects)} object(s)\n")
                for obj in objects:
                    size_kb = obj['Size'] / 1024
                    print(f"  • {obj['Key']}")
                    print(f"    Size: {size_kb:.2f} KB")
                    print(f"    Modified: {obj['LastModified']}")
                    print()
            
            return objects
        
        except ClientError as e:
            print(f"❌ Error listing state files: {e}")
            return None
    
    def get_state_file(self, state_key):
        """Download and parse Terraform state file"""
        if not self.state_bucket:
            print("❌ State bucket not configured")
            return None
        
        try:
            response = self.s3_client.get_object(Bucket=self.state_bucket, Key=state_key)
            state_content = response['Body'].read().decode('utf-8')
            state_json = json.loads(state_content)
            
            print(f"\n📋 Terraform State: {state_key}")
            print("-" * 80)
            print(f"  Terraform Version: {state_json.get('terraform_version', 'N/A')}")
            print(f"  Format Version: {state_json.get('version', 'N/A')}")
            print(f"  Resources: {len(state_json.get('resources', []))}")
            print(f"  Outputs: {len(state_json.get('outputs', {}))}")
            
            return state_json
        
        except ClientError as e:
            print(f"❌ Error getting state file: {e}")
            return None
    
    def list_terraform_resources(self, state_json):
        """List resources from Terraform state"""
        resources = state_json.get('resources', [])
        
        print(f"\n📦 Resources in state:")
        print("-" * 80)
        
        if not resources:
            print("  (No resources)")
        else:
            for resource in resources:
                resource_type = resource.get('type', 'unknown')
                instances = resource.get('instances', [])
                print(f"  • {resource_type} ({len(instances)} instance(s))")
                
                for instance in instances[:3]:  # Show first 3
                    instance_id = instance.get('attributes', {}).get('id', 'N/A')
                    print(f"    - {instance_id}")
                
                if len(instances) > 3:
                    print(f"    ... and {len(instances) - 3} more")
        
        return resources
    
    def list_vpc_resources(self):
        """List VPC resources in AWS account"""
        try:
            # VPCs
            vpcs = self.ec2_client.describe_vpcs()['Vpcs']
            
            print("\n" + "="*80)
            print("VPC RESOURCES".center(80))
            print("="*80 + "\n")
            
            print(f"✅ VPCs: {len(vpcs)}")
            for vpc in vpcs:
                print(f"  • {vpc['VpcId']} - {vpc['CidrBlock']}")
            
            # Subnets
            subnets = self.ec2_client.describe_subnets()['Subnets']
            print(f"\n✅ Subnets: {len(subnets)}")
            for subnet in subnets[:5]:
                print(f"  • {subnet['SubnetId']} - {subnet['CidrBlock']}")
            
            # Security Groups
            sgs = self.ec2_client.describe_security_groups()['SecurityGroups']
            print(f"\n✅ Security Groups: {len(sgs)}")
            for sg in sgs[:5]:
                print(f"  • {sg['GroupId']} - {sg['GroupName']}")
            
            return {
                'vpcs': len(vpcs),
                'subnets': len(subnets),
                'security_groups': len(sgs)
            }
        
        except ClientError as e:
            print(f"❌ Error listing resources: {e}")
            return None
    
    def create_state_backup(self, state_key, backup_key=None):
        """Create backup of Terraform state file"""
        if not self.state_bucket:
            print("❌ State bucket not configured")
            return False
        
        if not backup_key:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_key = f"{state_key}.backup.{timestamp}"
        
        try:
            copy_source = {'Bucket': self.state_bucket, 'Key': state_key}
            self.s3_client.copy_object(
                CopySource=copy_source,
                Bucket=self.state_bucket,
                Key=backup_key
            )
            print(f"✅ State backup created: {backup_key}")
            return True
        
        except ClientError as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def validate_state_bucket(self):
        """Validate Terraform state bucket configuration with proper error handling"""
        if not self.state_bucket:
            print("❌ State bucket not configured")
            return False
        
        try:
            self.s3_client.head_bucket(Bucket=self.state_bucket)
            print(f"✅ State bucket '{self.state_bucket}' is accessible")
            
            # Check versioning
            versioning = self.s3_client.get_bucket_versioning(Bucket=self.state_bucket)
            status = versioning.get('Status', 'Not enabled')
            print(f"   Versioning: {status}")
            
            # Check encryption - with proper exception handling
            try:
                encryption = self.s3_client.get_bucket_encryption(Bucket=self.state_bucket)
                print(f"   Encryption: Enabled")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    print(f"   Encryption: Not configured ⚠️")
                else:
                    print(f"   Encryption: Unable to verify ({e.response['Error']['Code']})")
            
            # Check public access block - with proper exception handling
            try:
                pab = self.s3_client.get_public_access_block(Bucket=self.state_bucket)
                config = pab.get('PublicAccessBlockConfiguration', {})
                all_blocked = all([
                    config.get('BlockPublicAcls', False),
                    config.get('BlockPublicPolicy', False),
                    config.get('IgnorePublicAcls', False),
                    config.get('RestrictPublicBuckets', False)
                ])
                status = "All blocked ✅" if all_blocked else "Partially blocked ⚠️"
                print(f"   Public Access: {status}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                    print(f"   Public Access: Not configured ⚠️ (Recommended to enable)")
                else:
                    print(f"   Public Access: Unable to verify ({e.response['Error']['Code']})")
            
            return True
        
        except ClientError as e:
            print(f"❌ Error validating bucket: {e}")
            return False

if __name__ == "__main__":
    manager = TerraformManager()
    
    print("\n" + "="*80)
    print("TERRAFORM MANAGER".center(80))
    print("="*80 + "\n")
    
    # List VPC resources
    manager.list_vpc_resources()
    
    print("\n✅ TerraformManager initialized")
    print("Usage examples:")
    print("  manager = TerraformManager(state_bucket='my-state-bucket')")
    print("  manager.list_state_files()")
    print("  manager.get_state_file('terraform.tfstate')")
    print("  manager.list_vpc_resources()")
    print("  manager.validate_state_bucket()")
