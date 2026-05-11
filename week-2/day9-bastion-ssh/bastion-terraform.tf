# Bastion Host Configuration with SSH Hardening
# Secure jumphost for accessing private resources

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "bastion_ami" {
  description = "Bastion AMI ID (Amazon Linux 2)"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}

variable "bastion_instance_type" {
  description = "Bastion instance type"
  type        = string
  default     = "t3.micro"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

# Data sources to get existing VPC and subnets
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["cloud-security-vpc"]
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
  
  filter {
    name   = "tag:Type"
    values = ["Public"]
  }
}

data "aws_security_group" "bastion" {
  vpc_id = data.aws_vpc.main.id
  
  filter {
    name   = "group-name"
    values = ["bastion-sg"]
  }
}

# IAM Role for Bastion
resource "aws_iam_role" "bastion" {
  name = "bastion-host-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "bastion-role"
  }
}

# Attach SSM policy for Systems Manager
resource "aws_iam_role_policy_attachment" "bastion_ssm" {
  role       = aws_iam_role.bastion.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Attach CloudWatch agent policy
resource "aws_iam_role_policy_attachment" "bastion_cloudwatch" {
  role       = aws_iam_role.bastion.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# Custom policy for Bastion
resource "aws_iam_role_policy" "bastion_custom" {
  name = "bastion-custom-policy"
  role = aws_iam_role.bastion.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeNetworkInterfaces"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:UpdateInstanceInformation",
          "ssmmessages:AcknowledgeMessage",
          "ssmmessages:GetEndpoint",
          "ssmmessages:GetMessages",
          "ec2messages:GetMessages"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:*:log-group:/aws/bastion/*"
      }
    ]
  })
}

# Instance profile
resource "aws_iam_instance_profile" "bastion" {
  name = "bastion-instance-profile"
  role = aws_iam_role.bastion.name
}

# CloudWatch Log Group for Bastion
resource "aws_cloudwatch_log_group" "bastion" {
  name              = "/aws/bastion/system-logs"
  retention_in_days = 30

  tags = {
    Name = "bastion-logs"
  }
}

# User data script for Bastion hardening
locals {
  user_data = base64encode(<<-EOF
    #!/bin/bash
    set -e
    
    # Update system
    yum update -y
    
    # Install required packages
    yum install -y \
      amazon-cloudwatch-agent \
      amazon-ec2-metadata-query \
      fail2ban \
      audit \
      curl \
      wget \
      git \
      htop \
      net-tools \
      nmap \
      telnet \
      python3 \
      python3-pip
    
    # SSH Hardening
    
    # Disable root login
    sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
    
    # Disable password authentication
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
    echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
    
    # Enable public key authentication
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
    
    # Protocol 2 only
    echo "Protocol 2" >> /etc/ssh/sshd_config
    
    # Disable X11 forwarding
    sed -i 's/X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config
    
    # Restrict authentication attempts
    echo "MaxAuthTries 3" >> /etc/ssh/sshd_config
    echo "MaxSessions 2" >> /etc/ssh/sshd_config
    
    # Idle timeout
    echo "ClientAliveInterval 300" >> /etc/ssh/sshd_config
    echo "ClientAliveCountMax 2" >> /etc/ssh/sshd_config
    
    # Strict mode
    echo "StrictModes yes" >> /etc/ssh/sshd_config
    
    # Host-based authentication
    echo "HostbasedAuthentication no" >> /etc/ssh/sshd_config
    
    # Verbose logging
    echo "LogLevel VERBOSE" >> /etc/ssh/sshd_config
    
    # Restart SSH service
    systemctl restart sshd
    
    # Configure Fail2Ban
    cat > /etc/fail2ban/jail.local << 'FAIL2BAN'
    [DEFAULT]
    bantime = 3600
    findtime = 600
    maxretry = 3
    
    [sshd]
    enabled = true
    port = ssh
    filter = sshd
    logpath = /var/log/auth.log
    maxretry = 3
    FAIL2BAN
    
    systemctl start fail2ban
    systemctl enable fail2ban
    
    # Configure auditd
    echo "-w /etc/ssh/sshd_config -p wa -k ssh_config_changes" >> /etc/audit/rules.d/audit.rules
    echo "-w /root/.ssh -p wa -k ssh_key_changes" >> /etc/audit/rules.d/audit.rules
    
    systemctl restart auditd
    systemctl enable auditd
    
    # Configure CloudWatch agent
    cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'CLOUDWATCH'
    {
      "logs": {
        "logs_collected": {
          "files": {
            "collect_list": [
              {
                "file_path": "/var/log/auth.log",
                "log_group_name": "/aws/bastion/auth-logs",
                "log_stream_name": "{instance_id}"
              },
              {
                "file_path": "/var/log/secure",
                "log_group_name": "/aws/bastion/secure-logs",
                "log_stream_name": "{instance_id}"
              }
            ]
          }
        }
      }
    }
    CLOUDWATCH
    
    # Start CloudWatch agent
    /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
      -a fetch-config \
      -m ec2 \
      -s \
      -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
    
    # Create bastion user
    useradd -m -s /bin/bash bastion || true
    usermod -aG wheel bastion || true
    
    # Configure sudo for bastion
    echo "bastion ALL=(ALL) NOPASSWD:ALL" | tee /etc/sudoers.d/bastion
    chmod 440 /etc/sudoers.d/bastion
    
    # Log setup completion
    echo "Bastion hardening completed at $(date)" >> /var/log/bastion-setup.log
  EOF
  )
}

# EC2 Key Pair
resource "aws_key_pair" "bastion" {
  key_name = "bastion-key"

  tags = {
    Name = "bastion-key"
  }
}

# Bastion EC2 Instance
resource "aws_instance" "bastion" {
  ami                         = var.bastion_ami
  instance_type               = var.bastion_instance_type
  subnet_id                   = data.aws_subnets.public.ids[0]
  vpc_security_group_ids      = [data.aws_security_group.bastion.id]
  iam_instance_profile        = aws_iam_instance_profile.bastion.name
  associate_public_ip_address = true
  user_data                   = local.user_data

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  monitoring = true

  tags = {
    Name        = "bastion-host"
    Purpose     = "Bastion-Host"
    Environment = var.environment
  }

  depends_on = [
    aws_iam_role_policy.bastion_custom,
    aws_iam_role_policy_attachment.bastion_ssm,
    aws_iam_role_policy_attachment.bastion_cloudwatch
  ]
}

# Elastic IP for Bastion
resource "aws_eip" "bastion" {
  instance = aws_instance.bastion.id
  domain   = "vpc"

  tags = {
    Name = "bastion-eip"
  }

  depends_on = [aws_instance.bastion]
}

# CloudWatch Alarm for Bastion CPU
resource "aws_cloudwatch_metric_alarm" "bastion_cpu" {
  alarm_name          = "bastion-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"

  dimensions = {
    InstanceId = aws_instance.bastion.id
  }

  alarm_description = "Alert when Bastion CPU exceeds 80%"
  treat_missing_data = "notBreaching"
}

# CloudWatch Alarm for Bastion Status
resource "aws_cloudwatch_metric_alarm" "bastion_status" {
  alarm_name          = "bastion-status-check"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "StatusCheckFailed"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "1"

  dimensions = {
    InstanceId = aws_instance.bastion.id
  }

  alarm_description = "Alert when Bastion status check fails"
  treat_missing_data = "notBreaching"
}

# Outputs
output "bastion_instance_id" {
  description = "Bastion instance ID"
  value       = aws_instance.bastion.id
}

output "bastion_public_ip" {
  description = "Bastion public IP"
  value       = aws_eip.bastion.public_ip
}

output "bastion_private_ip" {
  description = "Bastion private IP"
  value       = aws_instance.bastion.private_ip
}

output "bastion_security_group_id" {
  description = "Bastion security group ID"
  value       = data.aws_security_group.bastion.id
}

output "bastion_iam_role" {
  description = "Bastion IAM role name"
  value       = aws_iam_role.bastion.name
}

output "ssh_command" {
  description = "SSH command to connect to Bastion"
  value       = "ssh -i bastion-key.pem ec2-user@${aws_eip.bastion.public_ip}"
}

output "ssm_command" {
  description = "SSM Session Manager command"
  value       = "aws ssm start-session --target ${aws_instance.bastion.id}"
}
