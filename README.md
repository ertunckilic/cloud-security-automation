# Cloud Security Automation Engineer - 26-Week Roadmap

**Goal:** Get hired as Cloud Security Automation Engineer in 6 months  
**Status:** Week 2, Day 9 ✅  
**Location:** Turkey | Remote  
**Start Date:** 2026-04-26  
**Current Date:** 2026-05-11

---

## 📊 Overall Progress

Week 1: 7/7 days ✅ (100%)
Week 2: 2/5 days ✅ (40%)
Total:  9/26 = 35%

---

## 📅 Week 1 - Linux & AWS Fundamentals ✅

| Day | Topic | Status |
|-----|-------|--------|
| Day 1 | AWS Setup, GitHub SSH, Bandit 0-5 | ✅ |
| Day 2 | Bandit 6-10, Linux Permissions, Terraform | ✅ |
| Day 3 | Python Boto3 + AWS API Automation | ✅ |
| Day 4 | IAM Security Audit + Policy Management | ✅ |
| Day 5 | EC2-S3 Policies + Git Workflow | ✅ |
| Day 6 | MFA Setup + Security Policy + Automation | ✅ |
| Day 7 | CloudTrail & CloudWatch Monitoring | ✅ |

---

## 📅 Week 2 - Cloud Security & Networking 🔄

| Day | Topic | Status |
|-----|-------|--------|
| Day 8 | VPC & Network Security | ✅ |
| Day 9 | Bastion Host & SSH Hardening | ✅ |
| Day 10 | Auto Scaling & EC2 | ⏳ |
| Day 11 | RDS Database Security | ⏳ |
| Day 12 | Application Load Balancer (ALB) | ⏳ |

---

## 📁 Repository Structure

cloud-security-automation/
├── blog/
│   └── Day 2: Blog post - Linux mastery + AWS EC2 introduction
├── terraform/
│   └── day2-ec2/ - First Terraform EC2 configuration
├── week-1/
│   ├── day1-setup/
│   │   ├── aws-setup.md
│   │   ├── github-ssh.md
│   │   └── README.md
│   ├── day2-linux/
│   │   ├── bandit-solutions.md
│   │   ├── linux-permissions.md
│   │   └── README.md
│   ├── day3-boto3/
│   │   ├── boto3-basics.py
│   │   ├── aws-api-intro.py
│   │   └── README.md
│   ├── day4-iam/
│   │   ├── iam-audit.py
│   │   ├── security-policy.json
│   │   └── README.md
│   ├── day5-ec2-s3/
│   │   ├── ec2-s3-policy.json
│   │   ├── policy-implementation.py
│   │   └── README.md
│   ├── day6-mfa/
│   │   ├── mfa-policy.json
│   │   ├── mfa-best-practices.md
│   │   ├── check-mfa-status.py
│   │   ├── mfa-terraform.tf
│   │   └── README.md
│   └── day7-cloudtrail/
│       ├── setup-cloudtrail.py
│       ├── cloudwatch-monitoring.py
│       ├── cloudtrail-terraform.tf
│       └── README.md
├── week-2/
│   ├── day8-vpc-security/
│   │   ├── create-vpc.py
│   │   ├── security-groups-hardening.py
│   │   ├── vpc-terraform.tf
│   │   └── README.md
│   ├── day9-bastion-ssh/
│   │   ├── setup-bastion.py
│   │   ├── ssh-hardening.py
│   │   ├── bastion-terraform.tf
│   │   └── README.md
│   ├── day10-autoscaling/
│   ├── day11-rds/
│   └── day12-alb/
├── .gitignore
└── README.md

---

## ✅ Week 1 Key Accomplishments

### Day 1: AWS Setup & Linux Basics
- AWS account creation and configuration
- GitHub SSH key setup
- OverTheWire Bandit levels 0-5
- Linux command line fundamentals

### Day 2: Linux Mastery & Infrastructure as Code
- Bandit levels 6-10
- Linux file permissions (chmod, chown)
- First Terraform EC2 instance deployment
- Blog post: AWS EC2 introduction

### Day 3: Python Automation
- Python Boto3 basics
- AWS API integration
- Automation script creation
- EC2 instance management via API

### Day 4: IAM Security
- IAM security audit script created
- Security policies written
- Policy management automation
- User and group analysis

### Day 5: Cross-Service Security
- EC2-S3 cross-service policies
- Git workflow mastered
- Policy implementation
- Security best practices

### Day 6: Multi-Factor Authentication
- Virtual MFA device configured (Google Authenticator)
- MFA enforcement policy created
- Security automation scripts
- Terraform infrastructure as code

### Day 7: Audit & Monitoring
- CloudTrail logging enabled
- CloudWatch monitoring configured
- Log aggregation and analysis
- Security alerts setup

---

## ✅ Week 2 Key Accomplishments

### Day 8: VPC & Network Security
- VPC with CIDR 10.0.0.0/16
- Public Subnet: 10.0.1.0/24
- Private Subnet: 10.0.2.0/24
- Internet Gateway configured
- 4 Security Groups created
- NACLs configured
- VPC Flow Logs enabled
- 800+ lines of infrastructure code

### Day 9: Bastion Host & SSH Hardening
- Bastion EC2 instance in public subnet
- Elastic IP assigned for consistent access
- SSH hardening implemented:
  - Root login disabled
  - Password authentication disabled
  - Public key authentication only
  - Protocol 2 only
  - X11 forwarding disabled
  - Max auth tries: 3
  - Max sessions: 2
- auditd and Fail2Ban installed
- CloudWatch monitoring configured
- Systems Manager Session Manager enabled
- 1200+ lines of infrastructure code

---

## 🏗️ Technical Stack

| Component | Technology |
|-----------|-----------|
| Cloud Provider | AWS |
| Infrastructure as Code | Terraform |
| Automation | Python (Boto3) |
| Security | IAM, MFA, SSH, VPC |
| Monitoring | CloudTrail, CloudWatch |
| Logging | CloudWatch Logs, auditd |
| Version Control | Git / GitHub |
| Operating System | Kali Linux |
| SSH | OpenSSH with hardening |

---

## 📊 Statistics

- Total Days Completed: 9/26 (35%)
- Python Scripts: 15+
- Terraform Files: 8+
- Lines of Code: 5000+
- AWS Services Used: 12+
- Security Policies: 10+

---

## 🔒 Security Features Implemented

### Week 1
- ✅ IAM security audit
- ✅ MFA enforcement
- ✅ CloudTrail logging
- ✅ CloudWatch monitoring
- ✅ Security policies

### Week 2
- ✅ VPC with public/private subnets
- ✅ Security groups (4 types)
- ✅ Network ACLs (NACLs)
- ✅ Bastion host (jumphost)
- ✅ SSH hardening
- ✅ auditd monitoring
- ✅ Fail2Ban protection
- ✅ Systems Manager integration

---

## 🚀 Upcoming (Week 2 Remaining)

- [ ] Day 10: Auto Scaling & EC2
- [ ] Day 11: RDS Database Security
- [ ] Day 12: Application Load Balancer (ALB)

---

## 📚 Learning Objectives Achieved

- ✅ AWS fundamentals and account setup
- ✅ Linux security and permissions
- ✅ Python automation with Boto3
- ✅ IAM security best practices
- ✅ Terraform infrastructure as code
- ✅ Multi-factor authentication
- ✅ Security policy design
- ✅ Git workflow and version control
- ✅ VPC and network security
- ✅ SSH hardening and bastion hosts
- ✅ Audit logging and monitoring
- ✅ Compliance and best practices

---

## 🔗 Resources

- Linux Training: https://overthewire.org/wargames/bandit/
- AWS Documentation: https://docs.aws.amazon.com/
- Terraform: https://www.terraform.io/docs/
- SSH Security: https://infosec.mozilla.org/guidelines/openssh
- CIS Benchmarks: https://www.cisecurity.org/
- NIST Guidelines: https://nvlpubs.nist.gov/

---

## 👤 Author

Name: Ertunç Kılıç
GitHub: @ertunckilic
Location: Turkey
Start Date: 2026-04-26
Current Date: 2026-05-11

---

## 📄 License

MIT License - See LICENSE file for details

---

## 📞 Contact & Links

- GitHub Repository: cloud-security-automation
- GitHub Profile: ertunckilic

---

Last Updated: 2026-05-11
Progress: 9/26 Days (35%) ✅
Next Review: Week 2, Day 10 (2026-05-12)
