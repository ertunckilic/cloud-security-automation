# DAY 8: VPC & Network Security

## Overview

This day covers VPC setup with public/private subnets, security groups, and network access control lists (NACLs).

## What We Did

### 1. VPC Architecture
- Created VPC with CIDR 10.0.0.0/16
- Public subnet: 10.0.1.0/24 (AZ: eu-central-1a)
- Private subnet: 10.0.2.0/24 (AZ: eu-central-1b)
- Internet Gateway for public internet access
- Public and Private route tables

### 2. Security Groups
- Bastion Host SG (SSH access)
- Web Server SG (HTTP/HTTPS + Bastion SSH)
- Database Server SG (MySQL 3306 + Bastion SSH)
- ALB Security Group (HTTP/HTTPS)

### 3. Network ACLs (NACLs)
- Public NACL: HTTP, HTTPS, SSH, Ephemeral ports
- Private NACL: VPC CIDR traffic, Ephemeral ports
- Stateless rules configured

### 4. VPC Flow Logs
- CloudWatch log group for VPC Flow Logs
- IAM role for VPC Flow Logs
- Monitor all network traffic

### 5. Infrastructure as Code
- Terraform configuration for VPC
- Terraform configuration for Security Groups
- Terraform configuration for NACLs

## Files

week-2/day8-vpc-security/
├── create-vpc.py
├── security-groups-hardening.py
├── vpc-terraform.tf
└── README.md

## How to Use

### Step 1: Create VPC

cd ~/cloud-security-automation/week-2/day8-vpc-security
python3 create-vpc.py

### Step 2: Harden Security Groups

python3 security-groups-hardening.py

### Step 3: Deploy with Terraform

terraform init
terraform plan
terraform apply

## VPC Architecture Diagram

Internet
    |
    v
Internet Gateway (IGW)
    |
    +---> Public Subnet (10.0.1.0/24)
    |     - ALB
    |     - Bastion Host
    |     - Public Route Table
    |
    +---> Private Subnet (10.0.2.0/24)
          - Web Servers
          - Database Servers
          - Private Route Table

## Security Groups & Rules

### Bastion Security Group
- Inbound: SSH (22) from 0.0.0.0/0
- Outbound: All traffic

### Web Server Security Group
- Inbound: HTTP (80) from 0.0.0.0/0
- Inbound: HTTPS (443) from 0.0.0.0/0
- Inbound: SSH (22) from Bastion SG
- Outbound: All traffic

### Database Security Group
- Inbound: MySQL (3306) from Web SG
- Inbound: SSH (22) from Bastion SG
- Outbound: All traffic

### ALB Security Group
- Inbound: HTTP (80) from 0.0.0.0/0
- Inbound: HTTPS (443) from 0.0.0.0/0
- Outbound: All traffic

## Network ACL Rules

### Public NACL (Inbound)
- Rule 100: TCP 80 (HTTP) from 0.0.0.0/0 - ALLOW
- Rule 110: TCP 443 (HTTPS) from 0.0.0.0/0 - ALLOW
- Rule 120: TCP 22 (SSH) from 0.0.0.0/0 - ALLOW
- Rule 130: TCP 1024-65535 (Ephemeral) from 0.0.0.0/0 - ALLOW
- Rule 32767: All traffic - DENY

### Public NACL (Outbound)
- Rule 100: All traffic to 0.0.0.0/0 - ALLOW

### Private NACL (Inbound)
- Rule 100: All TCP from 10.0.0.0/16 (VPC CIDR) - ALLOW
- Rule 110: TCP 1024-65535 (Ephemeral) from 0.0.0.0/0 - ALLOW

### Private NACL (Outbound)
- Rule 100: All traffic to 0.0.0.0/0 - ALLOW

## VPC Flow Logs

- Log Group: /aws/vpc/flowlogs
- Traffic Type: ALL
- Retention: 30 days
- IAM Role: vpc-flow-logs-role

## Network Design Best Practices

DO:
- Use public subnets for load balancers and NAT
- Use private subnets for application servers
- Use private subnets for databases
- Implement bastion hosts for SSH access
- Use NACLs as second layer of defense
- Enable VPC Flow Logs
- Monitor traffic patterns
- Use least privilege principle

DON'T:
- Place databases in public subnets
- Allow SSH (22) from 0.0.0.0/0 except for Bastion
- Use overly permissive security group rules
- Disable NACLs
- Forget to enable VPC Flow Logs
- Use the same security group for multiple purposes
- Allow outbound traffic to 0.0.0.0/0 unnecessarily

## AWS Services Used

- VPC: Virtual Private Cloud
- Subnets: Public and Private
- IGW: Internet Gateway
- Route Tables: Public and Private
- Security Groups: Stateful firewall
- NACLs: Stateless firewall
- VPC Flow Logs: Network monitoring
- CloudWatch: Log storage

## Terraform Resources

- aws_vpc
- aws_subnet
- aws_internet_gateway
- aws_route_table
- aws_route_table_association
- aws_security_group
- aws_network_acl
- aws_flow_log
- aws_cloudwatch_log_group
- aws_iam_role
- aws_iam_role_policy

## Security Architecture

Layer 1: Internet Gateway
Layer 2: Network ACLs (Stateless)
Layer 3: Security Groups (Stateful)
Layer 4: Application-level controls

## Traffic Flow Examples

### HTTP Request Flow
1. Client -> Internet (0.0.0.0/0)
2. IGW receives on port 80
3. Public NACL checks inbound rule 100 (HTTP) - ALLOW
4. ALB SG checks inbound rule (HTTP from 0.0.0.0/0) - ALLOW
5. ALB routes to Web Server in Private Subnet
6. Private NACL checks inbound rule 100 (VPC CIDR) - ALLOW
7. Web SG checks inbound rule (HTTP from ALB SG) - ALLOW
8. Web Server processes request

### SSH to Web Server from Bastion
1. Bastion -> Web Server (Private IP)
2. VPC routes within private network
3. Private NACL checks inbound rule 100 (VPC CIDR) - ALLOW
4. Web SG checks inbound rule (SSH from Bastion SG) - ALLOW
5. SSH connection established

### Web Server to Database
1. Web Server -> Database (Private IP)
2. VPC routes within private network
3. Private NACL checks inbound rule 100 (VPC CIDR) - ALLOW
4. Database SG checks inbound rule (MySQL from Web SG) - ALLOW
5. Database connection established

## Monitoring & Troubleshooting

### View VPC Flow Logs
aws logs tail /aws/vpc/flowlogs --follow

### Check Security Group Rules
aws ec2 describe-security-groups --group-ids sg-xxxxxx

### Check Network ACL Rules
aws ec2 describe-network-acls --network-acl-ids acl-xxxxxx

### Test Connectivity
telnet <private-ip> 3306

## Compliance & Security

- Bastion host for SSH access (no direct access)
- Database isolated in private subnet
- NACLs provide stateless firewall
- Security Groups provide stateful firewall
- VPC Flow Logs for audit trail
- Least privilege access

## Next Steps (Week 2)

1. Deploy Bastion Host
2. Deploy Web Servers (Auto Scaling)
3. Deploy Database (RDS)
4. Configure ALB
5. Implement WAF

## Resources

- AWS VPC: https://docs.aws.amazon.com/vpc/
- Security Groups: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html
- Network ACLs: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html
- VPC Flow Logs: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
- Terraform AWS VPC: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc

## Author

- Created: 2026-05-10
- Status: Complete

DAY 8 COMPLETED SUCCESSFULLY!
