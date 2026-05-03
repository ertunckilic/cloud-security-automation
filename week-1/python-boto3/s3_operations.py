#!/usr/bin/env python3
"""
Day 3: S3 operations using Boto3
Learn: Upload, list, and delete S3 objects
"""

import boto3
from botocore.exceptions import ClientError
import os

def list_s3_buckets():
    """List all S3 buckets"""
    
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    try:
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        
        print("\n" + "="*80)
        print("S3 BUCKETS".center(80))
        print("="*80 + "\n")
        
        if not buckets:
            print("❌ No S3 buckets found")
        else:
            print(f"✅ Found {len(buckets)} bucket(s)\n")
            for bucket in buckets:
                print(f"  • {bucket['Name']} (Created: {bucket['CreationDate']})")
        
        return buckets
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

def list_s3_objects(bucket_name):
    """List objects in a specific bucket"""
    
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        
        print(f"\n📦 Objects in bucket '{bucket_name}':")
        print("-" * 80)
        
        if not objects:
            print("  (Empty bucket)")
        else:
            for obj in objects:
                size_mb = obj['Size'] / (1024 * 1024)
                print(f"  • {obj['Key']} ({size_mb:.2f} MB)")
        
        return objects
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

def upload_file_to_s3(bucket_name, file_path, object_name=None):
    """Upload a file to S3"""
    
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"✅ Successfully uploaded {file_path} to s3://{bucket_name}/{object_name}")
        return True
    
    except ClientError as e:
        print(f"❌ Error uploading file: {e}")
        return False

if __name__ == "__main__":
    # List all buckets
    buckets = list_s3_buckets()
    
    # If buckets exist, list objects in first bucket
    if buckets:
        first_bucket = buckets[0]['Name']
        list_s3_objects(first_bucket)
