#!/usr/bin/env python3
"""
Day 3: AWS Lambda automation using Boto3
Learn: List, invoke, and manage Lambda functions
"""

import boto3
import json
from botocore.exceptions import ClientError

class LambdaManager:
    """Manage AWS Lambda functions"""
    
    def __init__(self, region='us-east-1'):
        self.lambda_client = boto3.client('lambda', region_name=region)
    
    def list_functions(self):
        """List all Lambda functions"""
        try:
            response = self.lambda_client.list_functions()
            functions = response.get('Functions', [])
            
            print("\n" + "="*80)
            print("AWS LAMBDA FUNCTIONS".center(80))
            print("="*80 + "\n")
            
            if not functions:
                print("❌ No Lambda functions found")
            else:
                print(f"✅ Found {len(functions)} function(s)\n")
                for func in functions:
                    print(f"  • {func['FunctionName']}")
                    print(f"    Runtime: {func.get('Runtime', 'N/A')}")
                    print(f"    Handler: {func.get('Handler', 'N/A')}")
                    print(f"    Memory: {func.get('MemorySize', 'N/A')} MB")
                    print(f"    Timeout: {func.get('Timeout', 'N/A')} seconds")
                    print(f"    Last Modified: {func.get('LastModified', 'N/A')}")
                    print()
            
            return functions
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_function_info(self, function_name):
        """Get detailed info about a Lambda function"""
        try:
            response = self.lambda_client.get_function(FunctionName=function_name)
            config = response['Configuration']
            
            print(f"\n📋 Lambda Function: {function_name}")
            print("-" * 80)
            print(f"  ARN: {config['FunctionArn']}")
            print(f"  Runtime: {config.get('Runtime', 'N/A')}")
            print(f"  Handler: {config.get('Handler', 'N/A')}")
            print(f"  Memory: {config.get('MemorySize', 'N/A')} MB")
            print(f"  Timeout: {config.get('Timeout', 'N/A')} seconds")
            print(f"  Code Size: {config.get('CodeSize', 'N/A')} bytes")
            print(f"  State: {config.get('State', 'N/A')}")
            
            return config
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return None
    
    def invoke_function(self, function_name, payload=None):
        """Invoke a Lambda function"""
        try:
            if payload is None:
                payload = {}
            
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            status_code = response['StatusCode']
            
            print(f"\n✅ Lambda function invoked: {function_name}")
            print(f"   Status Code: {status_code}")
            
            if 'FunctionError' in response:
                print(f"   Error: {response['FunctionError']}")
            
            if 'Payload' in response:
                payload_data = json.loads(response['Payload'].read())
                print(f"   Response: {payload_data}")
            
            return response
        
        except ClientError as e:
            print(f"❌ Error invoking function: {e}")
            return None
    
    def list_function_configurations(self, function_name):
        """List all versions of a Lambda function"""
        try:
            response = self.lambda_client.list_versions_by_function(
                FunctionName=function_name
            )
            versions = response.get('Versions', [])
            
            print(f"\n📚 Versions for {function_name}:")
            print("-" * 80)
            
            for version in versions:
                print(f"  Version: {version['Version']}")
                print(f"    CodeSha256: {version['CodeSha256']}")
                print(f"    Last Modified: {version['LastModified']}")
            
            return versions
        
        except ClientError as e:
            print(f"❌ Error: {e}")
            return None

if __name__ == "__main__":
    manager = LambdaManager()
    
    print("\n" + "="*80)
    print("AWS LAMBDA AUTOMATION".center(80))
    print("="*80 + "\n")
    
    # List all functions
    manager.list_functions()
    
    print("✅ LambdaManager initialized")
    print("Usage examples:")
    print("  manager.get_function_info('function-name')")
    print("  manager.invoke_function('function-name', {'key': 'value'})")
    print("  manager.list_function_configurations('function-name')")
