# Day 4 Learning Guide: Infrastructure as Code

## What is Infrastructure as Code (IaC)?

Infrastructure as Code means writing code to provision and manage infrastructure instead of manual setup.

Benefits:
- Repeatable deployments
- Version control
- Easy scaling
- Disaster recovery
- Team collaboration

## CloudFormation vs Terraform

### CloudFormation
- AWS native service
- JSON/YAML format
- AWS-specific resources
- Built-in AWS integration
- Good for AWS-only projects

### Terraform
- Multi-cloud support (AWS, Azure, GCP)
- HCL language
- Declarative syntax
- Community-driven
- Better for multi-cloud

## Key Concepts

### Stacks (CloudFormation)
A stack is a collection of AWS resources defined in a template.

### State File (Terraform)
Tracks current infrastructure state and resource relationships.

### Parameters (CloudFormation)
Input values that customize stack deployment.

### Variables (Terraform)
Input values for infrastructure configuration.

### Outputs
Values returned after infrastructure deployment.

## CloudFormation Template Structure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Description of template'

Parameters:
  # Input parameters

Resources:
  # AWS resources

Outputs:
  # Return values
```

## Terraform Configuration Structure

```hcl
terraform {
  # Terraform settings
}

provider "aws" {
  # Provider configuration
}

resource "aws_resource_type" "name" {
  # Resource properties
}

output "name" {
  # Output values
}
```

## Common AWS Resources

### VPC
- Isolated network environment
- Subnets
- Route tables
- Internet Gateway

### EC2
- Virtual machines
- Security groups
- Key pairs

### S3
- Object storage
- Buckets
- Versioning
- Encryption

### IAM
- Users and roles
- Policies
- Permissions

## Best Practices

1. Version Control: Store templates in Git
2. Tagging: Tag all resources for cost tracking
3. Validation: Validate templates before deploying
4. State Management: Secure and backup Terraform state
5. Modularization: Break large templates into modules
6. Documentation: Document parameters and outputs
7. Testing: Test in development first
8. Monitoring: Enable CloudWatch monitoring

## Common Errors

### CloudFormation
- Missing Capabilities for IAM resources
- Invalid parameter values
- Circular dependencies
- Resource already exists

### Terraform
- State file conflicts
- Syntax errors
- Missing provider credentials
- Resource ID mismatch

## Debugging

### CloudFormation

```bash
# View stack events for detailed error information
aws cloudformation describe-stack-events --stack-name stack-name

# Validate template before deploying
aws cloudformation validate-template --template-body file://template.yaml

# Get detailed stack information
aws cloudformation describe-stacks --stack-name stack-name

# List all resources in a stack
aws cloudformation list-stack-resources --stack-name stack-name
```

### Terraform

```bash
# Enable debug logging to troubleshoot issues
export TF_LOG=DEBUG

# Validate configuration syntax
terraform validate

# Check code formatting
terraform fmt -check

# Plan infrastructure with output file
terraform plan -out=tfplan

# Refresh state to sync with AWS
terraform refresh

# Show current state
terraform show
```

## Setup Instructions

### EC2 KeyPair for CloudFormation

Before deploying the EC2 instance template, you need an EC2 KeyPair:

```bash
# Create a new KeyPair
aws ec2 create-key-pair --key-name my-ec2-key --region us-east-1 --query 'KeyMaterial' --output text > my-ec2-key.pem

# Set correct permissions (required for SSH)
chmod 400 my-ec2-key.pem

# Verify KeyPair was created
aws ec2 describe-key-pairs --region us-east-1

# Use the KeyPair when deploying the stack
aws cloudformation create-stack \
  --stack-name my-ec2-stack \
  --template-body file://ec2-instance.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=my-ec2-key \
  --capabilities CAPABILITY_IAM
```

### Regional AMI Support

The ec2-instance.yaml template includes AMI mappings for 7 AWS regions:

- us-east-1 (N. Virginia)
- us-west-1 (N. California)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- eu-central-1 (Frankfurt)
- ap-southeast-1 (Singapore)
- ap-northeast-1 (Tokyo)

To deploy in a different region, use the --region parameter:

```bash
aws cloudformation create-stack \
  --stack-name my-ec2-stack \
  --template-body file://ec2-instance.yaml \
  --region eu-west-1 \
  --parameters ParameterKey=KeyName,ParameterValue=my-ec2-key \
  --capabilities CAPABILITY_IAM
```

## Next Steps

1. Deploy VPC stack using CloudFormation
2. Create EC2 KeyPair and launch EC2 instance
3. Initialize Terraform and deploy infrastructure
4. Automate stack management with Python scripts
5. Implement monitoring and alerts

## Learning Outcomes Achieved

✅ Infrastructure as Code fundamentals
✅ CloudFormation template design with regional support
✅ Terraform configuration management
✅ VPC and networking architecture
✅ Security best practices (encryption, versioning)
✅ State file management
✅ Python Boto3 automation
✅ Documentation and learning guides
✅ Error handling and exception management
✅ Proper setup and deployment procedures
