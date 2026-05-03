#!/usr/bin/env python3
"""
Day 3: List EC2 instances using Boto3
Learn: How to connect to AWS and list resources
"""

import boto3
from botocore.exceptions import ClientError

def list_ec2_instances():
    """List all EC2 instances in AWS account"""
    
    # Create EC2 client
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    
    try:
        # Get all instances
        response = ec2_client.describe_instances()
        
        # Parse response
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'LaunchTime': instance['LaunchTime'],
                    'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                })
        
        # Print results
        print("\n" + "="*80)
        print("EC2 INSTANCES".center(80))
        print("="*80 + "\n")
        
        if not instances:
            print("❌ No EC2 instances found")
        else:
            print(f"✅ Found {len(instances)} instance(s)\n")
            for inst in instances:
                print(f"ID: {inst['InstanceId']}")
                print(f"  Type: {inst['InstanceType']}")
                print(f"  State: {inst['State']}")
                print(f"  Launch Time: {inst['LaunchTime']}")
                print(f"  Public IP: {inst['PublicIP']}")
                print()
        
        return instances
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    list_ec2_instances()
