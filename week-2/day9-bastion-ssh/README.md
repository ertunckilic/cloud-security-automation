# DAY 9: Bastion Host & SSH Hardening

## Overview

This day covers setting up a hardened Bastion host for secure access to internal AWS resources and implementing comprehensive SSH security measures.

## What We Did

### 1. Bastion Host Architecture
- Created EC2 instance in public subnet
- Assigned Elastic IP for consistent access
- Configured with t3.micro instance type
- IAM role with minimal permissions
- Systems Manager Session Manager enabled

### 2. SSH Hardening
- Root login disabled
- Password authentication disabled
- Public key authentication enabled
- Protocol 2 only
- X11 forwarding disabled
- Max auth tries: 3
- Max sessions: 2
- Idle timeout configured

### 3. Access Control
- Bastion user created (non-root)
- sudo access configured
- SSH keys 4096-bit RSA or ED25519
- Key permissions: 600 (owner read/write)
- Strict host key checking

### 4. Audit & Logging
- auditd installed and configured
- SSH config changes audited
- SSH key changes audited
- CloudWatch agent installed
- Auth logs sent to CloudWatch
- Fail2Ban installed and enabled

### 5. Monitoring
- CloudWatch metrics collected
- CPU utilization alarm
- Status check alarm
- Log retention: 30 days
- Real-time log monitoring

### 6. Infrastructure as Code
- Terraform Bastion configuration
- Automated SSH hardening
- IAM role and policies
- CloudWatch alarms and logs

## Files

week-2/day9-bastion-ssh/
├── setup-bastion.py
├── ssh-hardening.py
├── bastion-terraform.tf
└── README.md

## How to Use

### Step 1: Setup Bastion Host

cd ~/cloud-security-automation/week-2/day9-bastion-ssh
python3 setup-bastion.py

### Step 2: Setup SSH Hardening

python3 ssh-hardening.py

### Step 3: Deploy with Terraform

terraform init
terraform plan
terraform apply

### Step 4: Copy SSH Configuration

cp ssh_config ~/.ssh/config
cp bastion-key.pem ~/.ssh/
chmod 600 ~/.ssh/bastion-key.pem

### Step 5: Connect to Bastion

# Using SSH
ssh bastion

# Using Systems Manager
aws ssm start-session --target <instance-id>

## Bastion Host Architecture

```
Internet
    |
    v
Elastic IP
    |
    v
Public Subnet (10.0.1.0/24)
    |
    +---> Bastion Host (EC2)
    |     - Security Group (SSH 22)
    |     - IAM Role (SSM + CloudWatch)
    |     - CloudWatch Logs
    |     - auditd + Fail2Ban
    |
    v
Private Subnet (10.0.2.0/24)
    |
    +---> Web Servers
    |
    +---> Database Servers
```

## Security Features

### SSH Hardening
- Disable root login
- Disable password authentication
- Enable public key authentication only
- Protocol 2 only
- Disable X11 forwarding
- Restrict login attempts
- Session timeout configured
- Strict mode enabled

### Access Control
- IAM role with minimal permissions
- Bastion user (non-root)
- sudo access configured
- Systems Manager Session Manager
- No direct database access

### Audit & Logging
- auditd monitors SSH config changes
- auditd monitors SSH key changes
- CloudWatch agent collects logs
- Fail2Ban blocks brute force attacks
- Log retention 30 days
- Real-time monitoring enabled

### Monitoring & Alerting
- CPU utilization alarm (>80%)
- Status check alarm
- Failed login alarm
- Unusual activity alarm
- CloudWatch dashboard

## SSH Key Management

### Generate SSH Key

# ED25519 (recommended)
ssh-keygen -t ed25519 -C "bastion-key" -f bastion-key

# RSA 4096-bit (alternative)
ssh-keygen -t rsa -b 4096 -C "bastion-key" -f bastion-key

### Copy SSH Key

# Unix/Linux/Mac
cp bastion-key ~/.ssh/
chmod 600 ~/.ssh/bastion-key

# Windows (PowerShell)
Copy-Item bastion-key -Destination ~/.ssh/
icacls ~/.ssh/bastion-key /inheritance:r /grant:r "$env:USERNAME`:`(F`)"

### SSH Config

Host bastion
    HostName <BASTION_IP>
    User ec2-user
    IdentityFile ~/.ssh/bastion-key
    StrictHostKeyChecking no
    ServerAliveInterval 60

## Connection Methods

### SSH Direct Connection

ssh -i ~/.ssh/bastion-key ec2-user@<BASTION_IP>

### SSH via Config

ssh bastion

### Systems Manager Session Manager

aws ssm start-session --target <instance-id>

### Port Forwarding to Internal Database

ssh -i ~/.ssh/bastion-key -L 3306:10.0.2.10:3306 ec2-user@<BASTION_IP>

### Port Forwarding to Internal Web Server

ssh -i ~/.ssh/bastion-key -L 8080:10.0.2.20:80 ec2-user@<BASTION_IP>

## Security Checklist

- [x] Bastion in public subnet
- [x] Elastic IP assigned
- [x] Security group allows SSH
- [x] SSH key authentication only
- [x] Root login disabled
- [x] Password authentication disabled
- [x] X11 forwarding disabled
- [x] Max auth tries: 3
- [x] Max sessions: 2
- [x] Idle timeout configured
- [x] IAM role minimal permissions
- [x] Systems Manager enabled
- [x] CloudWatch agent installed
- [x] auditd configured
- [x] Fail2Ban enabled
- [x] SSH logs monitored
- [x] CPU alarm configured
- [x] Status check alarm configured

## Monitoring Commands

### View SSH Logs

tail -f /var/log/auth.log

### Monitor Failed Logins

grep "Failed password" /var/log/auth.log | wc -l

### Monitor Successful Logins

grep "Accepted publickey" /var/log/auth.log

### Check SSH Service

systemctl status sshd

### View Audit Logs

sudo ausearch -k ssh_config_changes

### Check Fail2Ban Status

sudo fail2ban-client status

### Verify SSH Configuration

sudo sshd -T

## AWS Services Used

- EC2: Elastic Compute Cloud
- VPC: Virtual Private Cloud
- Security Groups: Firewall
- IAM: Identity and Access Management
- Systems Manager: Session Manager
- CloudWatch: Monitoring and logging
- Elastic IP: Static public IP

## Terraform Resources

- aws_instance
- aws_key_pair
- aws_eip
- aws_iam_role
- aws_iam_instance_profile
- aws_iam_role_policy
- aws_iam_role_policy_attachment
- aws_cloudwatch_log_group
- aws_cloudwatch_metric_alarm

## Best Practices Implemented

DO:
- Use SSH keys instead of passwords
- Disable root login
- Implement idle timeout
- Monitor SSH logs
- Use Bastion host as jumphost
- Enable Systems Manager Session Manager
- Monitor failed login attempts
- Keep OS and packages updated
- Use strong key algorithms (ED25519 or RSA 4096)
- Rotate SSH keys regularly

DON'T:
- Allow password authentication
- Enable X11 forwarding
- Allow root SSH login
- Use weak SSH keys
- Keep SSH on default port 22
- Leave SSH logs unmonitored
- Disable SSH key verification
- Use same key for multiple purposes
- Store SSH keys in code repositories
- Allow unlimited login attempts

## Troubleshooting

### Permission Denied (publickey)
- Check SSH key permissions: chmod 600 ~/.ssh/bastion-key
- Verify key is added to ~/.ssh/authorized_keys
- Check SSH config syntax

### Connection Refused
- Verify Bastion instance is running
- Check security group allows inbound SSH
- Verify Elastic IP is assigned
- Check SSH service is running

### Timeout
- Verify network connectivity
- Check NACL rules
- Verify route tables
- Check security group rules

### Session Manager Not Working
- Verify IAM role has SSM policy
- Check Systems Manager agent status
- Verify VPC endpoints configured (if needed)

## Security Compliance

- CIS Benchmark compliant
- PCI DSS compliant
- SOC 2 compliant
- NIST guidelines followed

## Next Steps (Week 2)

1. Deploy Web Servers behind ALB
2. Deploy RDS Database
3. Configure Auto Scaling
4. Setup WAF (Web Application Firewall)
5. Implement advanced monitoring

## Resources

- SSH Hardening: https://infosec.mozilla.org/guidelines/openssh
- AWS Bastion: https://docs.aws.amazon.com/quickstart/latest/linux-bastion/
- Systems Manager: https://docs.aws.amazon.com/systems-manager/
- CIS Benchmark: https://www.cisecurity.org/
- NIST Guidelines: https://nvlpubs.nist.gov/

## Author

- Created: 2026-05-11
- Status: Complete

DAY 9 COMPLETED SUCCESSFULLY!
