# Day 3: Python Boto3 - AWS API Automation

## Overview
Day 3 focuses on learning AWS API automation using Python Boto3. We created 7 scripts to interact with different AWS services.

## Scripts Created

### 1. list_ec2.py
Lists all EC2 instances in your AWS account.

Usage: python list_ec2.py

Features:
- Connects to EC2 service
- Lists all instances with details (ID, Type, State, IP)
- Handles errors gracefully

### 2. s3_operations.py
Manages S3 buckets and objects.

Usage: python s3_operations.py

Features:
- List all S3 buckets
- List objects in specific bucket
- Upload files to S3

### 3. ec2_automation.py
Automates EC2 instance management.

Usage: python ec2_automation.py

EC2Manager Class Methods:
- start_instance(instance_id)
- stop_instance(instance_id)
- reboot_instance(instance_id)
- get_instance_status(instance_id)
- create_snapshot(volume_id)

### 4. iam_operations.py
Query IAM users, roles, and account information.

Usage: python iam_operations.py

Features:
- List IAM users
- List IAM roles
- Get AWS account ID

### 5. cloudwatch_monitoring.py
Monitor EC2 instances with CloudWatch.

Usage: python cloudwatch_monitoring.py

Features:
- Get EC2 metrics (CPU, Network, etc)
- List CloudWatch alarms
- Create CPU utilization alarms

### 6. security_groups.py
Manage EC2 security groups and firewall rules.

Usage: python security_groups.py

SecurityGroupManager Class Methods:
- list_security_groups()
- get_security_group_rules(group_id)
- authorize_ssh(group_id, cidr)
- authorize_http(group_id, cidr)
- authorize_https(group_id, cidr)

### 7. lambda_automation.py
Manage AWS Lambda functions.

Usage: python lambda_automation.py

LambdaManager Class Methods:
- list_functions()
- get_function_info(function_name)
- invoke_function(function_name, payload)
- list_function_configurations(function_name)

## Setup

Prerequisites:
- Python 3.9+
- AWS Account with credentials
- boto3 library

Installation:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

AWS Credentials Setup:
Create ~/.aws/credentials file:

[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-1

Or use environment variables:
export AWS_ACCESS_KEY_ID=your_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

## Running Scripts

python list_ec2.py
python s3_operations.py
python ec2_automation.py
python iam_operations.py
python cloudwatch_monitoring.py
python security_groups.py
python lambda_automation.py

## Learning Outcomes

✅ How to use Boto3 library
✅ AWS service connectivity
✅ Error handling with botocore
✅ Programmatic AWS resource management
✅ Class-based automation patterns
✅ Client vs Resource patterns
✅ Security best practices
