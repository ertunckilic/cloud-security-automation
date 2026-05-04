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
aws cloudformation describe-stack-events --stack-name stack-name
aws cloudformation validate-template --template-body file://template.yaml

### Terraform
export TF_LOG=DEBUG
terraform validate
terraform plan -out=tfplan

## Next Steps

1. Deploy VPC stack using CloudFormation
2. Launch EC2 instance with CloudFormation
3. Initialize Terraform and deploy infrastructure
4. Automate stack management with Python scripts
5. Implement CI/CD pipeline for IaC
