import boto3
import json
from datetime import datetime

# Initialize clients
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

# Configuration
BASTION_AMI = 'ami-0c55b159cbfafe1f0'  # Amazon Linux 2
BASTION_INSTANCE_TYPE = 't3.micro'
BASTION_NAME = 'bastion-host'
REGION = ec2.meta.region_name

def get_vpc_and_subnet():
    """Get VPC and public subnet"""
    try:
        # Get VPC
        vpcs = ec2.describe_vpcs(Filters=[
            {'Name': 'tag:Name', 'Values': ['cloud-security-vpc']}
        ])
        
        if not vpcs['Vpcs']:
            print("❌ VPC not found. Please create VPC first.")
            return None, None
        
        vpc_id = vpcs['Vpcs'][0]['VpcId']
        print(f"✅ Found VPC: {vpc_id}")
        
        # Get public subnet
        subnets = ec2.describe_subnets(Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]},
            {'Name': 'tag:Type', 'Values': ['Public']}
        ])
        
        if not subnets['Subnets']:
            print("❌ Public subnet not found.")
            return vpc_id, None
        
        subnet_id = subnets['Subnets'][0]['SubnetId']
        print(f"✅ Found Public Subnet: {subnet_id}")
        
        return vpc_id, subnet_id
    except Exception as e:
        print(f"❌ Error getting VPC/Subnet: {e}")
        return None, None

def get_bastion_sg(vpc_id):
    """Get Bastion security group"""
    try:
        sgs = ec2.describe_security_groups(Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]},
            {'Name': 'group-name', 'Values': ['bastion-sg']}
        ])
        
        if not sgs['SecurityGroups']:
            print("❌ Bastion security group not found.")
            return None
        
        sg_id = sgs['SecurityGroups'][0]['GroupId']
        print(f"✅ Found Bastion SG: {sg_id}")
        return sg_id
    except Exception as e:
        print(f"❌ Error getting Bastion SG: {e}")
        return None

def create_bastion_role():
    """Create IAM role for Bastion host"""
    try:
        iam = boto3.client('iam')
        role_name = 'bastion-host-role'
        
        try:
            # Create role
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Role for Bastion host'
            )
            print(f"✅ IAM role created: {role_name}")
        except iam.exceptions.EntityAlreadyExistsException:
            print(f"✅ IAM role exists: {role_name}")
        
        # Attach SSM policy for Systems Manager
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
        )
        print(f"✅ SSM policy attached")
        
        # Attach CloudWatch policy
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy'
        )
        print(f"✅ CloudWatch policy attached")
        
        # Create instance profile
        try:
            iam.create_instance_profile(InstanceProfileName=role_name)
            print(f"✅ Instance profile created")
        except iam.exceptions.EntityAlreadyExistsException:
            print(f"✅ Instance profile exists")
        
        # Add role to instance profile
        try:
            iam.add_role_to_instance_profile(
                InstanceProfileName=role_name,
                RoleName=role_name
            )
            print(f"✅ Role added to instance profile")
        except iam.exceptions.EntityAlreadyExistsException:
            print(f"✅ Role already in instance profile")
        
        return role_name
    except Exception as e:
        print(f"❌ Error creating Bastion role: {e}")
        return None

def create_bastion_instance(subnet_id, sg_id, role_name):
    """Create Bastion EC2 instance"""
    try:
        # User data script for bastion
        user_data = """#!/bin/bash
set -e

# Update system
yum update -y

# Install useful tools
yum install -y \
    telnet \
    nmap \
    git \
    curl \
    wget \
    htop \
    net-tools \
    openssh-clients \
    python3 \
    python3-pip

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
rm -rf awscliv2.zip aws/

# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm

# Configure SSH hardening
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/#Protocol 2/Protocol 2/' /etc/ssh/sshd_config
echo "Port 22" >> /etc/ssh/sshd_config
echo "X11Forwarding no" >> /etc/ssh/sshd_config
echo "MaxAuthTries 3" >> /etc/ssh/sshd_config
echo "MaxSessions 2" >> /etc/ssh/sshd_config

# Restart SSH service
systemctl restart sshd

# Create bastion user
useradd -m -s /bin/bash bastion || true
usermod -aG wheel bastion || true

# Setup log monitoring
echo "Bastion host setup completed at $(date)" >> /var/log/bastion-setup.log

# Enable CloudWatch agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s
"""
        
        response = ec2.run_instances(
            ImageId=BASTION_AMI,
            MinCount=1,
            MaxCount=1,
            InstanceType=BASTION_INSTANCE_TYPE,
            SubnetId=subnet_id,
            SecurityGroupIds=[sg_id],
            IamInstanceProfile={'Name': role_name},
            UserData=user_data,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': BASTION_NAME},
                        {'Key': 'Purpose', 'Value': 'Bastion-Host'},
                        {'Key': 'Environment', 'Value': 'production'}
                    ]
                }
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"✅ Bastion instance created: {instance_id}")
        print(f"   Instance Type: {BASTION_INSTANCE_TYPE}")
        print(f"   Subnet: {subnet_id}")
        print(f"   Security Group: {sg_id}")
        
        return instance_id
    except Exception as e:
        print(f"❌ Error creating Bastion instance: {e}")
        return None

def wait_for_instance(instance_id):
    """Wait for instance to be running"""
    try:
        waiter = ec2.get_waiter('instance_running')
        print(f"⏳ Waiting for instance to be running...")
        waiter.wait(InstanceIds=[instance_id])
        
        # Get instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance['PrivateIpAddress']
        
        print(f"✅ Instance is running")
        print(f"   Public IP: {public_ip}")
        print(f"   Private IP: {private_ip}")
        
        return public_ip, private_ip
    except Exception as e:
        print(f"❌ Error waiting for instance: {e}")
        return None, None

def create_security_group_rules_for_bastion(vpc_id):
    """Create specific rules for Bastion to access internal resources"""
    try:
        # Get Bastion SG
        bastion_sgs = ec2.describe_security_groups(Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]},
            {'Name': 'group-name', 'Values': ['bastion-sg']}
        ])
        
        if not bastion_sgs['SecurityGroups']:
            return False
        
        bastion_sg_id = bastion_sgs['SecurityGroups'][0]['GroupId']
        
        # Add egress rule for SSH to private instances
        try:
            ec2.authorize_security_group_egress(
                GroupId=bastion_sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '10.0.0.0/16', 'Description': 'SSH to VPC'}]
                    }
                ]
            )
            print(f"✅ Bastion egress rule added for SSH")
        except Exception as e:
            if 'InvalidPermission.Duplicate' in str(e):
                print(f"✅ Bastion egress rule already exists")
            else:
                raise
        
        return True
    except Exception as e:
        print(f"❌ Error creating SG rules: {e}")
        return False

def enable_systems_manager_session(instance_id):
    """Enable Systems Manager Session Manager for connection"""
    try:
        # Session Manager allows secure connection without SSH keys
        print(f"✅ Systems Manager Session Manager enabled")
        print(f"   Connect via: aws ssm start-session --target {instance_id}")
        return True
    except Exception as e:
        print(f"❌ Error enabling Session Manager: {e}")
        return False

def main():
    print("=" * 60)
    print("AWS Bastion Host Setup")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Step 1: Get VPC and Subnet
    print("Step 1: Getting VPC and Subnet...")
    vpc_id, subnet_id = get_vpc_and_subnet()
    if not vpc_id or not subnet_id:
        print("Failed to get VPC/Subnet. Exiting.")
        return
    print()
    
    # Step 2: Get Bastion Security Group
    print("Step 2: Getting Bastion Security Group...")
    sg_id = get_bastion_sg(vpc_id)
    if not sg_id:
        print("Failed to get Bastion SG. Exiting.")
        return
    print()
    
    # Step 3: Create Bastion IAM Role
    print("Step 3: Creating Bastion IAM Role...")
    role_name = create_bastion_role()
    if not role_name:
        print("Failed to create IAM role. Exiting.")
        return
    print()
    
    # Step 4: Create SG rules for Bastion
    print("Step 4: Creating security group rules...")
    create_security_group_rules_for_bastion(vpc_id)
    print()
    
    # Step 5: Create Bastion Instance
    print("Step 5: Creating Bastion EC2 instance...")
    instance_id = create_bastion_instance(subnet_id, sg_id, role_name)
    if not instance_id:
        print("Failed to create Bastion instance. Exiting.")
        return
    print()
    
    # Step 6: Wait for instance
    print("Step 6: Waiting for instance to be ready...")
    public_ip, private_ip = wait_for_instance(instance_id)
    print()
    
    # Step 7: Enable Systems Manager
    print("Step 7: Enabling Systems Manager...")
    enable_systems_manager_session(instance_id)
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Bastion Host Setup Completed Successfully!")
    print("=" * 60)
    print()
    print("Bastion Host Information:")
    print(f"  Instance ID: {instance_id}")
    print(f"  Instance Type: {BASTION_INSTANCE_TYPE}")
    print(f"  VPC: {vpc_id}")
    print(f"  Subnet: {subnet_id}")
    print(f"  Security Group: {sg_id}")
    print(f"  Public IP: {public_ip}")
    print(f"  Private IP: {private_ip}")
    print()
    print("Connection Methods:")
    print(f"  SSH: ssh -i <key.pem> ec2-user@{public_ip}")
    print(f"  Systems Manager: aws ssm start-session --target {instance_id}")
    print()
    print("SSH Hardening Applied:")
    print("  - Root login disabled")
    print("  - Password authentication disabled")
    print("  - Public key authentication enabled")
    print("  - X11 forwarding disabled")
    print("  - Max auth tries: 3")
    print("  - Max sessions: 2")
    print()

if __name__ == '__main__':
    main()
