import boto3
import json
from datetime import datetime
import subprocess
import os

# Initialize clients
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def create_key_pair(key_name):
    """Create EC2 key pair"""
    try:
        response = ec2.create_key_pair(KeyName=key_name)
        private_key = response['KeyMaterial']
        
        # Save private key to file
        key_path = f"{key_name}.pem"
        with open(key_path, 'w') as f:
            f.write(private_key)
        
        # Set correct permissions
        os.chmod(key_path, 0o400)
        
        print(f"✅ Key pair created: {key_name}")
        print(f"   Saved to: {key_path}")
        return key_name
    except ec2.exceptions.InvalidKeyPair.Duplicate:
        print(f"✅ Key pair already exists: {key_name}")
        return key_name
    except Exception as e:
        print(f"❌ Error creating key pair: {e}")
        return None

def generate_ssh_config():
    """Generate SSH configuration file"""
    try:
        ssh_config = """# SSH Configuration for Bastion Host

Host bastion
    HostName <BASTION_IP>
    User ec2-user
    IdentityFile ~/.ssh/bastion-key.pem
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    LogLevel QUIET
    ConnectionAttempts 3
    ConnectTimeout 10
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Access internal servers through Bastion
Host 10.0.2.*
    ProxyCommand ssh -q bastion nc -q0 %h %p
    User ec2-user
    IdentityFile ~/.ssh/bastion-key.pem
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
"""
        
        config_path = "ssh_config"
        with open(config_path, 'w') as f:
            f.write(ssh_config)
        
        print(f"✅ SSH config generated: {config_path}")
        return config_path
    except Exception as e:
        print(f"❌ Error generating SSH config: {e}")
        return None

def create_ssh_hardening_policy():
    """Create SSH hardening policy document"""
    try:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowSSMConnection",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:UpdateInstanceInformation",
                        "ssmmessages:AcknowledgeMessage",
                        "ssmmessages:GetEndpoint",
                        "ssmmessages:GetMessages",
                        "ec2messages:GetMessages"
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "AllowEC2Describe",
                    "Effect": "Allow",
                    "Action": [
                        "ec2:DescribeInstances",
                        "ec2:DescribeSecurityGroups"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        policy_path = "ssh-hardening-policy.json"
        with open(policy_path, 'w') as f:
            json.dump(policy, f, indent=2)
        
        print(f"✅ SSH hardening policy created: {policy_path}")
        return policy
    except Exception as e:
        print(f"❌ Error creating policy: {e}")
        return None

def create_ssh_hardening_guide():
    """Create SSH hardening guide"""
    try:
        guide = """# SSH Hardening Guide for Bastion Host

## SSH Configuration Best Practices

### 1. Public Key Authentication
- Use strong RSA keys (4096-bit minimum)
- Or use ED25519 keys (recommended)
- Never use password authentication

### 2. SSH Server Hardening (/etc/ssh/sshd_config)

# Disable root login
PermitRootLogin no

# Disable password authentication
PasswordAuthentication no
PubkeyAuthentication yes

# Restrict protocol version
Protocol 2

# Disable X11 forwarding
X11Forwarding no

# Limit login attempts
MaxAuthTries 3
MaxSessions 2

# Strict mode
StrictModes yes

# Disable empty password
PermitEmptyPasswords no

# Disable host-based authentication
HostbasedAuthentication no

# Enable logging
SyslogFacility AUTH
LogLevel VERBOSE

# Idle timeout
ClientAliveInterval 300
ClientAliveCountMax 2

# Port (change from 22 to non-standard)
Port 22222

### 3. SSH Client Hardening

# Use SSH keys only
Host *
    PubkeyAuthentication yes
    PasswordAuthentication no

# Strict host key checking
Host *
    StrictHostKeyChecking accept-new
    UpdateHostKeys yes

# Disable unused authentication methods
Host *
    KbdInteractiveAuthentication no
    GSSAPIAuthentication no

### 4. Key Management

# Generate ED25519 key (recommended)
ssh-keygen -t ed25519 -C "bastion-key" -f bastion-key

# Generate RSA key (4096-bit)
ssh-keygen -t rsa -b 4096 -C "bastion-key" -f bastion-key

# Set correct permissions
chmod 600 bastion-key
chmod 644 bastion-key.pub

### 5. SSH Tunneling through Bastion

# Port forwarding to internal database
ssh -i bastion-key -L 3306:10.0.2.10:3306 ec2-user@bastion-ip

# Port forwarding to internal web server
ssh -i bastion-key -L 8080:10.0.2.20:80 ec2-user@bastion-ip

### 6. Session Recording (with auditd)

# Install auditd
sudo yum install audit -y

# Add audit rule for SSH
echo "-w /etc/ssh/sshd_config -p wa -k ssh_config_changes" | sudo tee -a /etc/audit/rules.d/audit.rules

# Restart auditd
sudo service auditd restart

### 7. Fail2Ban Setup

# Install fail2ban
sudo yum install fail2ban -y

# Create SSH jail config
sudo cat > /etc/fail2ban/jail.local << EOF
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
findtime = 600
bantime = 3600
EOF

# Start fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

### 8. SSH Banner

# Create banner file
sudo nano /etc/ssh/banner

# Add to /etc/ssh/sshd_config
Banner /etc/ssh/banner

### 9. SSH Monitoring

# View SSH logs
sudo tail -f /var/log/auth.log

# Monitor failed login attempts
sudo grep "Failed password" /var/log/auth.log | wc -l

# Monitor successful logins
sudo grep "Accepted publickey" /var/log/auth.log

### 10. Two-Factor Authentication (2FA)

# Install Google Authenticator
sudo yum install google-authenticator -y

# Initialize 2FA for user
google-authenticator

# Enable PAM for SSH 2FA
# Edit /etc/ssh/sshd_config
# Add: AuthenticationMethods publickey,keyboard-interactive:pam

## Security Checklist

- [ ] SSH running on non-standard port
- [ ] Root login disabled
- [ ] Password authentication disabled
- [ ] Public key authentication enabled
- [ ] X11 forwarding disabled
- [ ] Protocol 2 only
- [ ] Max auth tries set to 3
- [ ] SSH keys are 4096-bit RSA or ED25519
- [ ] Key permissions are 600
- [ ] Auditd installed and configured
- [ ] Fail2Ban installed and enabled
- [ ] SSH banner configured
- [ ] SSH logs monitored
- [ ] 2FA enabled (optional but recommended)

## Monitoring Commands

# List active SSH sessions
ps aux | grep sshd

# Monitor SSH attempts
tail -f /var/log/auth.log | grep ssh

# Check SSH configuration
sudo sshd -T

# Test SSH configuration
sudo sshd -t

# View SSH service status
sudo systemctl status sshd

## Emergency Access

If locked out:
1. Use EC2 Instance Connect (if enabled)
2. Use Systems Manager Session Manager
3. Use EC2 User Data to reset SSH config
4. Reattach volume to another instance

## Resources

- SSH Hardening Guide: https://infosec.mozilla.org/guidelines/openssh
- CIS Benchmark: https://www.cisecurity.org/
- NIST Guidelines: https://nvlpubs.nist.gov/
"""
        
        guide_path = "SSH-HARDENING-GUIDE.md"
        with open(guide_path, 'w') as f:
            f.write(guide)
        
        print(f"✅ SSH hardening guide created: {guide_path}")
        return guide_path
    except Exception as e:
        print(f"❌ Error creating guide: {e}")
        return None

def create_bastion_security_audit():
    """Create bastion security audit checklist"""
    try:
        audit = """# Bastion Host Security Audit Checklist

## 1. Network Security

- [ ] Bastion in public subnet
- [ ] Public IP assigned
- [ ] Security group allows SSH from restricted IPs
- [ ] Security group allows SSH to private instances
- [ ] NACLs configured correctly
- [ ] VPC Flow Logs enabled
- [ ] No unnecessary open ports

## 2. SSH Hardening

- [ ] SSH on non-standard port (not 22)
- [ ] Root login disabled
- [ ] Password authentication disabled
- [ ] Public key authentication enabled
- [ ] X11 forwarding disabled
- [ ] Protocol 2 only
- [ ] Max auth tries: 3
- [ ] Max sessions: 2
- [ ] Idle timeout configured
- [ ] Strict mode enabled
- [ ] Host key algorithms configured

## 3. Access Control

- [ ] IAM role with minimal permissions
- [ ] EC2 Systems Manager enabled
- [ ] Session Manager Session Manager configured
- [ ] Session logs sent to CloudWatch
- [ ] Session recordings enabled
- [ ] No direct database access from bastion

## 4. Audit Logging

- [ ] CloudWatch agent installed
- [ ] Auditd installed
- [ ] SSH audit rules configured
- [ ] Fail2Ban installed
- [ ] Log retention configured
- [ ] CloudWatch alarms set
- [ ] SNS notifications configured

## 5. Package Management

- [ ] OS patches applied
- [ ] Security updates installed
- [ ] Unnecessary packages removed
- [ ] Package manager updated
- [ ] Automatic updates enabled

## 6. Authentication & Authorization

- [ ] SSH keys 4096-bit RSA or ED25519
- [ ] Key permissions 600 (owner read/write)
- [ ] Public key permissions 644
- [ ] Bastion user created (not root)
- [ ] Sudo access configured
- [ ] 2FA enabled (optional)
- [ ] SSH banner configured

## 7. Monitoring & Alerting

- [ ] CloudWatch metrics collected
- [ ] CPU usage alarm
- [ ] Memory usage alarm
- [ ] Disk usage alarm
- [ ] Network alarm
- [ ] Failed login alarm
- [ ] Unusual activity alarm

## 8. Backup & Disaster Recovery

- [ ] AMI snapshot created
- [ ] Configuration backed up
- [ ] SSH keys backed up securely
- [ ] Recovery procedure documented

## 9. Compliance

- [ ] PCI DSS compliant
- [ ] SOC 2 compliant
- [ ] HIPAA compliant (if applicable)
- [ ] CIS Benchmark compliant
- [ ] Security policy documented

## 10. Incident Response

- [ ] Response plan documented
- [ ] Escalation procedure defined
- [ ] Contact list created
- [ ] Forensics procedure defined
- [ ] Backup bastion available

## Regular Maintenance

- [ ] Review logs weekly
- [ ] Update OS monthly
- [ ] Review IAM permissions quarterly
- [ ] Test DR procedures annually
- [ ] Review security posture quarterly
"""
        
        audit_path = "BASTION-SECURITY-AUDIT.md"
        with open(audit_path, 'w') as f:
            f.write(audit)
        
        print(f"✅ Security audit checklist created: {audit_path}")
        return audit_path
    except Exception as e:
        print(f"❌ Error creating audit: {e}")
        return None

def main():
    print("=" * 60)
    print("SSH Hardening & Key Management Setup")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Step 1: Generate SSH key
    print("Step 1: Generating SSH key pair...")
    key_name = "bastion-key"
    create_key_pair(key_name)
    print()
    
    # Step 2: Generate SSH config
    print("Step 2: Generating SSH config...")
    generate_ssh_config()
    print()
    
    # Step 3: Create SSH hardening policy
    print("Step 3: Creating SSH hardening policy...")
    create_ssh_hardening_policy()
    print()
    
    # Step 4: Create SSH hardening guide
    print("Step 4: Creating SSH hardening guide...")
    create_ssh_hardening_guide()
    print()
    
    # Step 5: Create security audit checklist
    print("Step 5: Creating security audit checklist...")
    create_bastion_security_audit()
    print()
    
    # Summary
    print("=" * 60)
    print("✅ SSH Hardening Setup Completed!")
    print("=" * 60)
    print()
    print("Generated Files:")
    print(f"  - {key_name}.pem (SSH private key)")
    print(f"  - ssh_config (SSH configuration)")
    print(f"  - ssh-hardening-policy.json (IAM policy)")
    print(f"  - SSH-HARDENING-GUIDE.md (Complete guide)")
    print(f"  - BASTION-SECURITY-AUDIT.md (Audit checklist)")
    print()
    print("Next Steps:")
    print(f"  1. Copy SSH config: cp ssh_config ~/.ssh/config")
    print(f"  2. Copy SSH key: cp {key_name}.pem ~/.ssh/")
    print(f"  3. Set permissions: chmod 600 ~/.ssh/{key_name}.pem")
    print(f"  4. Test connection: ssh bastion")
    print()

if __name__ == '__main__':
    main()
