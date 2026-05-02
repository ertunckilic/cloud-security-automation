# Day 2: First Terraform EC2 Deployment

This Terraform configuration deploys:
- VPC (10.0.0.0/16)
- Internet Gateway
- Public Subnet (10.0.1.0/24)
- Security Group (SSH + HTTP)
- EC2 Instance (t2.micro - Free Tier)

## Usage

terraform init
terraform plan
terraform apply
terraform destroy

## What we learn:
- Terraform basics (HCL syntax)
- VPC + Networking
- EC2 instances
- Security groups
- Infrastructure as Code
