# Day 2: Linux Mastery + First AWS Infrastructure

Date: April 27, 2026
Status: Week 1, Day 2
Theme: Linux Deep Dive + AWS EC2 Basics

## Today's Accomplishments

1. OverTheWire Bandit levels 6-10 (advanced Linux)
2. Linux permissions mastery (chmod, chown, chgrp)
3. First AWS EC2 configuration (Terraform)
4. VPC networking setup
5. 3 GitHub commits

Time Invested: 4 hours
GitHub Commits: 3

## What I Learned Today

### Linux Advanced Commands (Bandit 6-10)

Level 6 - File Finding by Attributes:
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null

Level 7 - Text Searching:
grep "millionth" data.txt

Level 8 - Unique Line Finding:
sort data.txt | uniq -u

### Linux File Permissions Deep Dive

Permission Numbers:
- 755 = rwxr-xr-x (scripts, executables)
- 644 = rw-r--r-- (regular files)
- 600 = rw------- (sensitive files, SSH keys)
- 700 = rwx------ (private directories)

Real Examples:
chmod 755 script.sh        # Executable by all
chmod 644 config.txt       # Readable by all
chmod 600 ~/.ssh/id_ed25519 # SSH key (owner only!)
chmod 700 ~/.ssh/           # SSH directory (owner only!)

### AWS EC2 + Terraform Introduction

What is Terraform?
- Infrastructure as Code (IaC) tool
- Define AWS resources in code
- Repeatable, version-controlled deployments

What I deployed:
VPC (10.0.0.0/16)
  - Internet Gateway
  - Public Subnet (10.0.1.0/24)
  - Route Table
  - Security Group
  - EC2 Instance (t2.micro)

## Key Insights

1. Linux is everything - 80% of cloud infrastructure runs Linux
2. Permissions matter - Most security breaches involve permission misconfigurations
3. Automation is key - Manual deployments don't scale
4. Code > Clicks - Infrastructure as Code is the future

## Tomorrow's Goals (Day 3)

- OverTheWire Bandit levels 11-15
- Python boto3 basics (AWS API)
- Deploy EC2 instance with Terraform
- SSH into instance + harden
- 3+ more GitHub commits

## Takeaway

Master the fundamentals, automate everything else.

Today I went deeper into Linux (the foundation) and started with Infrastructure as Code (the automation). These two skills are the backbone of cloud security engineering.

Follow my journey:
- GitHub: https://github.com/ertunckilicAct/cloud-security-automation
- Blog: /blog folder
- LinkedIn: ertunckilic

Day 3 coming tomorrow!
