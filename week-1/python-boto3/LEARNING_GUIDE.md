# Week 1 - Day 3: Python Boto3 Learning Guide

## What is Boto3?

Boto3 is the AWS SDK for Python. It allows you to write software that uses AWS services like Amazon EC2, Amazon S3, and more.

## Key Concepts

### 1. AWS Services Used
- EC2 - Elastic Compute Cloud (virtual servers)
- S3 - Simple Storage Service (object storage)
- IAM - Identity and Access Management
- CloudWatch - Monitoring and logging
- Lambda - Serverless compute
- Security Groups - Virtual firewalls

### 2. Boto3 Patterns

Client Pattern:
import boto3
client = boto3.client('ec2', region_name='us-east-1')

Resource Pattern:
import boto3
ec2 = boto3.resource('ec2', region_name='us-east-1')

### 3. Error Handling
from botocore.exceptions import ClientError

try:
    response = client.describe_instances()
except ClientError as e:
    print(f"Error: {e}")

## Scripts Overview

### 1. list_ec2.py
Purpose: List all EC2 instances
Output: Instance ID, Type, State, Public IP

### 2. s3_operations.py
Purpose: Manage S3 buckets and objects
Functions: List buckets, list objects, upload files

### 3. ec2_automation.py
Purpose: Automate EC2 management
Methods: Start, stop, reboot, snapshot creation

### 4. iam_operations.py
Purpose: Query IAM users and roles
Output: Account ID, User ARN, Role information

### 5. cloudwatch_monitoring.py
Purpose: Monitor EC2 with CloudWatch
Features: Get metrics, list alarms, create alarms

### 6. security_groups.py
Purpose: Manage security groups
Methods: List groups, view rules, authorize ports

### 7. lambda_automation.py
Purpose: Manage Lambda functions
Methods: List functions, invoke, get info

## AWS Credentials Setup

Create ~/.aws/credentials:

[default]
aws_access_key_id = YOUR_KEY_ID
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-1

## Running Scripts

python list_ec2.py
python s3_operations.py
python cloudwatch_monitoring.py
python security_groups.py
python lambda_automation.py
python iam_operations.py

## Best Practices

1. Always use error handling (try-except)
2. Never hardcode credentials
3. Use IAM roles on EC2 instances
4. Monitor costs with CloudWatch
5. Stop unused instances to save costs

## Learning Outcomes

✅ Understanding Boto3
✅ AWS service connectivity
✅ Error handling
✅ Resource management
✅ Automation workflows
✅ Security best practices
