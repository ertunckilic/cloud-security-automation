#!/usr/bin/env python3
"""
Day 3: Security Group management using Boto3
Learn: Create, modify, and manage security groups
"""

import boto3
from botocore.exceptions import ClientError

class SecurityGroupManager:
    """Manage EC2 security groups"""
    
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.resource('ec2', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
    
    def list_security_groups(self):
        """List all security groups"""
        try:
            response = self.ec2_client.describe_security_groups()
            groups = response.get('SecurityGroups', [])
            
            print("\n" + "="*80)
            print("SECURITY GROUPS".center(80))
            print("="*80 + "\n")
            
            if not groups:
                print("❌ No security groups found")
            else:
                print(f"✅ Found {len(groups)} security group(s)\n")
                for group in groups:
                    print(f"  • {group['GroupName']} ({group['GroupId']})")
                    print(f"    VPC: {group.get('VpcId', 'N/A')}")
                    print(f"    Description: {group.get('GroupDescription', 'N/A')}")
                    print(f"    Rules: {len(group.get('IpPermissions', []))} inbound")
                    print()
            
            return groups
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_security_group_rules(self, group_id):
        """Get detailed rules for a security group"""
        try:
            response = self.ec2_client.describe_security_groups(GroupIds=[group_id])
            group = response['SecurityGroups'][0]
            
            print(f"\n📋 Security Group: {group['GroupName']} ({group_id})")
            print("-" * 80)
            
            # Inbound rules
            print("\n📥 Inbound Rules:")
            inbound = group.get('IpPermissions', [])
            if not inbound:
                print("  (No rules)")
            else:
                for rule in inbound:
                    protocol = rule.get('IpProtocol', 'N/A')
                    from_port = rule.get('FromPort', 'N/A')
                    to_port = rule.get('ToPort', 'N/A')
                    cidr = rule.get('IpRanges', [{}])[0].get('CidrIp', 'N/A')
                    
                    print(f"  • Protocol: {protocol}, Ports: {from_port}-{to_port}, CIDR: {cidr}")
            
            # Outbound rules
            print("\n📤 Outbound Rules:")
            outbound = group.get('IpPermissionsEgress', [])
            if not outbound:
                print("  (No rules)")
            else:
                for rule in outbound[:3]:  # Show first 3
                    protocol = rule.get('IpProtocol', 'N/A')
                    cidr = rule.get('IpRanges', [{}])[0].get('CidrIp', 'N/A')
                    print(f"  • Protocol: {protocol}, CIDR: {cidr}")
                if len(outbound) > 3:
                    print(f"  ... and {len(outbound) - 3} more")
            
            return group
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return None
    
    def authorize_ssh(self, group_id, cidr='0.0.0.0/0'):
        """Allow SSH access (port 22)"""
        try:
            self.ec2_client.authorize_security_group_ingress(
                GroupId=group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': cidr, 'Description': 'SSH access'}]
                    }
                ]
            )
            print(f"✅ SSH access authorized for {cidr} in {group_id}")
            return True
        
        except ClientError as e:
            if 'InvalidPermission.Duplicate' in str(e):
                print(f"ℹ️  SSH rule already exists")
            else:
                print(f"❌ Error: {e}")
            return False
    
    def authorize_http(self, group_id, cidr='0.0.0.0/0'):
        """Allow HTTP access (port 80)"""
        try:
            self.ec2_client.authorize_security_group_ingress(
                GroupId=group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': cidr, 'Description': 'HTTP access'}]
                    }
                ]
            )
            print(f"✅ HTTP access authorized for {cidr} in {group_id}")
            return True
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return False
    
    def authorize_https(self, group_id, cidr='0.0.0.0/0'):
        """Allow HTTPS access (port 443)"""
        try:
            self.ec2_client.authorize_security_group_ingress(
                GroupId=group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 443,
                        'ToPort': 443,
                        'IpRanges': [{'CidrIp': cidr, 'Description': 'HTTPS access'}]
                    }
                ]
            )
            print(f"✅ HTTPS access authorized for {cidr} in {group_id}")
            return True
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    manager = SecurityGroupManager()
    
    print("\n" + "="*80)
    print("SECURITY GROUP MANAGER".center(80))
    print("="*80 + "\n")
    
    # List all security groups
    manager.list_security_groups()
    
    print("\n✅ SecurityGroupManager initialized")
    print("Usage examples:")
    print("  manager.get_security_group_rules('sg-xxxxx')")
    print("  manager.authorize_ssh('sg-xxxxx')")
    print("  manager.authorize_http('sg-xxxxx')")
