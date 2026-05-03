#!/usr/bin/env python3
"""
Day 3: EC2 automation - Start/Stop instances
Learn: Control EC2 instances programmatically
"""

import boto3
from botocore.exceptions import ClientError
import sys

class EC2Manager:
    """Manage EC2 instances"""
    
    def __init__(self, region='us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.ec2_resource = boto3.resource('ec2', region_name=region)
    
    def start_instance(self, instance_id):
        """Start an EC2 instance"""
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            print(f"✅ Starting instance {instance_id}...")
            return True
        except ClientError as e:
            print(f"❌ Error starting instance: {e}")
            return False
    
    def stop_instance(self, instance_id):
        """Stop an EC2 instance"""
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            print(f"✅ Stopping instance {instance_id}...")
            return True
        except ClientError as e:
            print(f"❌ Error stopping instance: {e}")
            return False
    
    def reboot_instance(self, instance_id):
        """Reboot an EC2 instance"""
        try:
            self.ec2_client.reboot_instances(InstanceIds=[instance_id])
            print(f"✅ Rebooting instance {instance_id}...")
            return True
        except ClientError as e:
            print(f"❌ Error rebooting instance: {e}")
            return False
    
    def get_instance_status(self, instance_id):
        """Get instance status"""
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            print(f"\n📊 Instance Status: {instance_id}")
            print("-" * 60)
            print(f"  State: {instance['State']['Name']}")
            print(f"  Type: {instance['InstanceType']}")
            print(f"  Public IP: {instance.get('PublicIpAddress', 'N/A')}")
            print(f"  Launch Time: {instance['LaunchTime']}")
            
            return instance['State']['Name']
        
        except ClientError as e:
            print(f"❌ Error getting status: {e}")
            return None
    
    def create_snapshot(self, volume_id, description="Automated snapshot"):
        """Create snapshot from volume"""
        try:
            response = self.ec2_client.create_snapshot(
                VolumeId=volume_id,
                Description=description
            )
            snapshot_id = response['SnapshotId']
            print(f"✅ Creating snapshot {snapshot_id} from volume {volume_id}...")
            return snapshot_id
        except ClientError as e:
            print(f"❌ Error creating snapshot: {e}")
            return None

if __name__ == "__main__":
    manager = EC2Manager()
    
    print("\n" + "="*80)
    print("EC2 AUTOMATION MANAGER".center(80))
    print("="*80 + "\n")
    
    print("✅ EC2Manager initialized successfully")
    print("Usage examples:")
    print("  manager.start_instance('i-xxxxx')")
    print("  manager.stop_instance('i-xxxxx')")
    print("  manager.get_instance_status('i-xxxxx')")
    print("  manager.create_snapshot('vol-xxxxx')")
