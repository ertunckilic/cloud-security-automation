# Day 3: Python Boto3 - AWS API Automation

## Overview
Day 3 focuses on learning AWS API automation using Python Boto3. We created 4 scripts to interact with different AWS services.

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

## Setup

Prerequisites:
- Python 3.9+
- AWS Account with credentials
- boto3 library

Installation:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Learning Outcomes

✅ How to use Boto3 library
✅ AWS service connectivity
✅ Error handling with botocore
✅ Programmatic AWS resource management
