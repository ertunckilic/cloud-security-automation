# Day 4: Infrastructure as Code (CloudFormation & Terraform)

## Overview
Day 4 focuses on Infrastructure as Code using CloudFormation and Terraform. We created templates and automation scripts for AWS infrastructure provisioning.

## CloudFormation Templates

### 1. vpc-stack.yaml
Creates a complete VPC infrastructure with public and private subnets.

Features:
- VPC with customizable CIDR block
- Internet Gateway
- Public and Private subnets
- Route tables and associations
- Outputs for resource references

### 2. ec2-instance.yaml
Launches an EC2 instance with security group and IAM role.

Features:
- Security group with HTTP, HTTPS, SSH rules
- IAM role for EC2
- UserData script for Apache setup
- Customizable instance type
- Tag configuration

### 3. s3-bucket.yaml
Creates an S3 bucket with versioning and encryption.

Features:
- Versioning enabled
- AES256 encryption
- Public access blocked
- Bucket policy for SSL enforcement

## Terraform Configuration

### main.tf
Main infrastructure configuration:
- VPC and subnets
- Internet Gateway
- Route tables
- Security groups
- S3 bucket for state management

### variables.tf
Input variables with validation

### outputs.tf
Output values for infrastructure

### terraform.tfvars
Default variable values

## Python Scripts

### cloudformation_manager.py
Methods:
- create_stack()
- list_stacks()
- describe_stack()
- get_stack_resources()
- delete_stack()
- wait_for_stack()

### terraform_manager.py
Methods:
- list_state_files()
- get_state_file()
- list_terraform_resources()
- list_vpc_resources()
- create_state_backup()
- validate_state_bucket()

## Learning Outcomes

✅ CloudFormation template syntax
✅ Infrastructure as Code concepts
✅ VPC and networking setup
✅ EC2 instance provisioning
✅ S3 bucket configuration
✅ Terraform state management
✅ Automation with Python Boto3
