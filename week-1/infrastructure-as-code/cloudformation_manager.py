#!/usr/bin/env python3
"""
Day 4: CloudFormation stack management using Boto3
Learn: Create, update, delete, and monitor CloudFormation stacks
"""

import boto3
from botocore.exceptions import ClientError
import json
import time

class CloudFormationManager:
    """Manage CloudFormation stacks"""
    
    def __init__(self, region='us-east-1'):
        self.cf_client = boto3.client('cloudformation', region_name=region)
    
    def create_stack(self, stack_name, template_body, parameters=None):
        """Create a new CloudFormation stack"""
        try:
            kwargs = {
                'StackName': stack_name,
                'TemplateBody': template_body,
                'Capabilities': ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']
            }
            
            if parameters:
                kwargs['Parameters'] = parameters
            
            response = self.cf_client.create_stack(**kwargs)
            stack_id = response['StackId']
            
            print(f"✅ Stack creation initiated: {stack_name}")
            print(f"   Stack ID: {stack_id}")
            return stack_id
        
        except ClientError as e:
            print(f"❌ Error creating stack: {e}")
            return None
    
    def list_stacks(self):
        """List all CloudFormation stacks"""
        try:
            response = self.cf_client.list_stacks(
                StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE']
            )
            stacks = response.get('StackSummaries', [])
            
            print("\n" + "="*80)
            print("CLOUDFORMATION STACKS".center(80))
            print("="*80 + "\n")
            
            if not stacks:
                print("❌ No stacks found")
            else:
                print(f"✅ Found {len(stacks)} stack(s)\n")
                for stack in stacks:
                    print(f"  • {stack['StackName']}")
                    print(f"    Status: {stack['StackStatus']}")
                    print(f"    Created: {stack['CreationTime']}")
                    print()
            
            return stacks
        
        except ClientError as e:
            print(f"❌ Error listing stacks: {e}")
            return None
    
    def describe_stack(self, stack_name):
        """Get detailed information about a stack"""
        try:
            response = self.cf_client.describe_stacks(StackName=stack_name)
            stack = response['Stacks'][0]
            
            print(f"\n📋 CloudFormation Stack: {stack_name}")
            print("-" * 80)
            print(f"  Stack ID: {stack['StackId']}")
            print(f"  Status: {stack['StackStatus']}")
            print(f"  Created: {stack['CreationTime']}")
            
            if 'LastUpdatedTime' in stack:
                print(f"  Last Updated: {stack['LastUpdatedTime']}")
            
            # Parameters
            if 'Parameters' in stack:
                print(f"\n  Parameters:")
                for param in stack['Parameters']:
                    print(f"    - {param['ParameterKey']}: {param['ParameterValue']}")
            
            # Outputs
            if 'Outputs' in stack:
                print(f"\n  Outputs:")
                for output in stack['Outputs']:
                    print(f"    - {output['OutputKey']}: {output['OutputValue']}")
            
            return stack
        
        except ClientError as e:
            print(f"❌ Error describing stack: {e}")
            return None
    
    def get_stack_resources(self, stack_name):
        """List resources in a stack"""
        try:
            response = self.cf_client.list_stack_resources(StackName=stack_name)
            resources = response.get('StackResourceSummaries', [])
            
            print(f"\n📦 Resources in stack '{stack_name}':")
            print("-" * 80)
            
            if not resources:
                print("  (No resources)")
            else:
                for resource in resources:
                    print(f"  • {resource['LogicalResourceId']}")
                    print(f"    Type: {resource['ResourceType']}")
                    print(f"    Status: {resource['ResourceStatus']}")
                    print(f"    Physical ID: {resource['PhysicalResourceId']}")
                    print()
            
            return resources
        
        except ClientError as e:
            print(f"❌ Error listing resources: {e}")
            return None
    
    def delete_stack(self, stack_name):
        """Delete a CloudFormation stack"""
        try:
            self.cf_client.delete_stack(StackName=stack_name)
            print(f"✅ Stack deletion initiated: {stack_name}")
            return True
        
        except ClientError as e:
            print(f"❌ Error deleting stack: {e}")
            return False
    
    def wait_for_stack(self, stack_name, action='create'):
        """Wait for stack operation to complete"""
        try:
            waiter_name = f'stack_{action}_complete'
            waiter = self.cf_client.get_waiter(waiter_name)
            
            print(f"\n⏳ Waiting for stack {action} to complete...")
            waiter.wait(StackName=stack_name)
            
            print(f"✅ Stack {action} completed successfully!")
            return True
        
        except ClientError as e:
            print(f"❌ Error waiting for stack: {e}")
            return False

if __name__ == "__main__":
    manager = CloudFormationManager()
    
    print("\n" + "="*80)
    print("CLOUDFORMATION MANAGER".center(80))
    print("="*80 + "\n")
    
    # List stacks
    manager.list_stacks()
    
    print("\n✅ CloudFormationManager initialized")
    print("Usage examples:")
    print("  manager.create_stack('stack-name', template_body)")
    print("  manager.describe_stack('stack-name')")
    print("  manager.get_stack_resources('stack-name')")
    print("  manager.delete_stack('stack-name')")
