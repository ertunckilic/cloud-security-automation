#!/usr/bin/env python3
"""
Day 3: IAM operations using Boto3
Learn: List users, roles, and policies
"""

import boto3
from botocore.exceptions import ClientError

def list_iam_users():
    """List all IAM users"""
    
    iam_client = boto3.client('iam')
    
    try:
        response = iam_client.list_users()
        users = response.get('Users', [])
        
        print("\n" + "="*80)
        print("IAM USERS".center(80))
        print("="*80 + "\n")
        
        if not users:
            print("❌ No IAM users found")
        else:
            print(f"✅ Found {len(users)} user(s)\n")
            for user in users:
                print(f"  • {user['UserName']}")
                print(f"    ARN: {user['Arn']}")
                print(f"    Created: {user['CreateDate']}")
                print()
        
        return users
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

def list_iam_roles():
    """List all IAM roles"""
    
    iam_client = boto3.client('iam')
    
    try:
        response = iam_client.list_roles()
        roles = response.get('Roles', [])
        
        print("\n" + "="*80)
        print("IAM ROLES".center(80))
        print("="*80 + "\n")
        
        if not roles:
            print("❌ No IAM roles found")
        else:
            print(f"✅ Found {len(roles)} role(s)\n")
            for role in roles:
                print(f"  • {role['RoleName']}")
                print(f"    ARN: {role['Arn']}")
                print(f"    Created: {role['CreateDate']}")
                print()
        
        return roles
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

def get_account_info():
    """Get AWS account information"""
    
    sts_client = boto3.client('sts')
    
    try:
        identity = sts_client.get_caller_identity()
        
        print("\n" + "="*80)
        print("AWS ACCOUNT INFO".center(80))
        print("="*80 + "\n")
        
        print(f"  Account ID: {identity['Account']}")
        print(f"  User ARN: {identity['Arn']}")
        print(f"  ✅ Successfully connected to AWS")
        
        return identity
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Get account info
    get_account_info()
    
    # List users and roles
    list_iam_users()
    list_iam_roles()
