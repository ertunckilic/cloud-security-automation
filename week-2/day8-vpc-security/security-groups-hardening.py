import boto3
import json
from datetime import datetime

# Initialize client
ec2 = boto3.client('ec2')

def create_bastion_security_group(vpc_id):
    """Create Bastion host security group"""
    try:
        response = ec2.create_security_group(
            GroupName='bastion-sg',
            Description='Security group for Bastion host',
            VpcId=vpc_id
        )
        sg_id = response['GroupId']
        
        # Tag security group
        ec2.create_tags(
            Resources=[sg_id],
            Tags=[
                {'Key': 'Name', 'Value': 'bastion-sg'},
                {'Key': 'Purpose', 'Value': 'Bastion-Host'}
            ]
        )
        
        # SSH from anywhere (restrict this in production!)
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'SSH from anywhere'}]
                }
            ]
        )
        
        print(f"✅ Bastion security group created: {sg_id}")
        print(f"   Inbound: SSH (22) from 0.0.0.0/0")
        return sg_id
    except Exception as e:
        print(f"❌ Error creating bastion security group: {e}")
        return None

def create_web_security_group(vpc_id):
    """Create Web server security group"""
    try:
        response = ec2.create_security_group(
            GroupName='web-sg',
            Description='Security group for Web servers',
            VpcId=vpc_id
        )
        sg_id = response['GroupId']
        
        # Tag security group
        ec2.create_tags(
            Resources=[sg_id],
            Tags=[
                {'Key': 'Name', 'Value': 'web-sg'},
                {'Key': 'Purpose', 'Value': 'Web-Servers'}
            ]
        )
        
        # HTTP from anywhere
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTP'}]
                }
            ]
        )
        
        # HTTPS from anywhere
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTPS'}]
                }
            ]
        )
        
        print(f"✅ Web security group created: {sg_id}")
        print(f"   Inbound: HTTP (80), HTTPS (443)")
        return sg_id
    except Exception as e:
        print(f"❌ Error creating web security group: {e}")
        return None

def create_database_security_group(vpc_id):
    """Create Database security group"""
    try:
        response = ec2.create_security_group(
            GroupName='database-sg',
            Description='Security group for Database servers',
            VpcId=vpc_id
        )
        sg_id = response['GroupId']
        
        # Tag security group
        ec2.create_tags(
            Resources=[sg_id],
            Tags=[
                {'Key': 'Name', 'Value': 'database-sg'},
                {'Key': 'Purpose', 'Value': 'Database-Servers'}
            ]
        )
        
        # MySQL/Aurora from web-sg only
        # This will be configured after web-sg is created
        
        print(f"✅ Database security group created: {sg_id}")
        print(f"   Inbound: MySQL (3306) from web-sg (to be configured)")
        return sg_id
    except Exception as e:
        print(f"❌ Error creating database security group: {e}")
        return None

def create_alb_security_group(vpc_id):
    """Create ALB security group"""
    try:
        response = ec2.create_security_group(
            GroupName='alb-sg',
            Description='Security group for Application Load Balancer',
            VpcId=vpc_id
        )
        sg_id = response['GroupId']
        
        # Tag security group
        ec2.create_tags(
            Resources=[sg_id],
            Tags=[
                {'Key': 'Name', 'Value': 'alb-sg'},
                {'Key': 'Purpose', 'Value': 'Load-Balancer'}
            ]
        )
        
        # HTTP from anywhere
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTP'}]
                }
            ]
        )
        
        # HTTPS from anywhere
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTPS'}]
                }
            ]
        )
        
        print(f"✅ ALB security group created: {sg_id}")
        print(f"   Inbound: HTTP (80), HTTPS (443)")
        return sg_id
    except Exception as e:
        print(f"❌ Error creating ALB security group: {e}")
        return None

def configure_sg_rules(web_sg_id, db_sg_id, alb_sg_id, bastion_sg_id):
    """Configure security group rules between groups"""
    try:
        # Web from ALB
        ec2.authorize_security_group_ingress(
            GroupId=web_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'UserIdGroupPairs': [{'GroupId': alb_sg_id, 'Description': 'HTTP from ALB'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'UserIdGroupPairs': [{'GroupId': alb_sg_id, 'Description': 'HTTPS from ALB'}]
                }
            ]
        )
        print(f"✅ Web SG: Added ingress rules from ALB")
        
        # Database from Web
        ec2.authorize_security_group_ingress(
            GroupId=db_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3306,
                    'ToPort': 3306,
                    'UserIdGroupPairs': [{'GroupId': web_sg_id, 'Description': 'MySQL from Web'}]
                }
            ]
        )
        print(f"✅ Database SG: Added ingress rule from Web (MySQL 3306)")
        
        # Web SSH from Bastion
        ec2.authorize_security_group_ingress(
            GroupId=web_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'UserIdGroupPairs': [{'GroupId': bastion_sg_id, 'Description': 'SSH from Bastion'}]
                }
            ]
        )
        print(f"✅ Web SG: Added SSH rule from Bastion")
        
        # Database SSH from Bastion
        ec2.authorize_security_group_ingress(
            GroupId=db_sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'UserIdGroupPairs': [{'GroupId': bastion_sg_id, 'Description': 'SSH from Bastion'}]
                }
            ]
        )
        print(f"✅ Database SG: Added SSH rule from Bastion")
        
        return True
    except Exception as e:
        print(f"❌ Error configuring SG rules: {e}")
        return False

def create_nacl(vpc_id, subnet_id):
    """Create Network ACL (hardened)"""
    try:
        response = ec2.create_network_acl(VpcId=vpc_id)
        nacl_id = response['NetworkAcl']['NetworkAclId']
        
        # Tag NACL
        ec2.create_tags(
            Resources=[nacl_id],
            Tags=[
                {'Key': 'Name', 'Value': 'hardened-nacl'},
                {'Key': 'Purpose', 'Value': 'Network-Protection'}
            ]
        )
        
        # Inbound rules
        # HTTP
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=100,
            Protocol='6',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
            PortRange={'From': 80, 'To': 80}
        )
        
        # HTTPS
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=110,
            Protocol='6',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
            PortRange={'From': 443, 'To': 443}
        )
        
        # SSH
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=120,
            Protocol='6',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
            PortRange={'From': 22, 'To': 22}
        )
        
        # Ephemeral ports
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=130,
            Protocol='6',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
            PortRange={'From': 1024, 'To': 65535}
        )
        
        # ICMP for ping
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=140,
            Protocol='1',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
            IcmpTypeCode={'Type': -1, 'Code': -1}
        )
        
        # Deny all other inbound traffic
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=32767,
            Protocol='-1',
            RuleAction='deny',
            CidrBlock='0.0.0.0/0'
        )
        
        # Outbound rules (allow all for simplicity)
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=100,
            Protocol='-1',
            Egress=True,
            RuleAction='allow',
            CidrBlock='0.0.0.0/0'
        )
        
        print(f"✅ Network ACL created: {nacl_id}")
        return nacl_id
    except Exception as e:
        print(f"❌ Error creating NACL: {e}")
        return None

def main():
    print("=" * 60)
    print("AWS Security Groups & NACLs Hardening")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Get VPC ID from user
    vpc_id = input("Enter VPC ID (or press Enter to skip): ").strip()
    if not vpc_id:
        print("Skipping security group creation")
        return
    print()
    
    # Step 1: Create Bastion SG
    print("Step 1: Creating Bastion security group...")
    bastion_sg_id = create_bastion_security_group(vpc_id)
    if not bastion_sg_id:
        return
    print()
    
    # Step 2: Create Web SG
    print("Step 2: Creating Web security group...")
    web_sg_id = create_web_security_group(vpc_id)
    if not web_sg_id:
        return
    print()
    
    # Step 3: Create Database SG
    print("Step 3: Creating Database security group...")
    db_sg_id = create_database_security_group(vpc_id)
    if not db_sg_id:
        return
    print()
    
    # Step 4: Create ALB SG
    print("Step 4: Creating ALB security group...")
    alb_sg_id = create_alb_security_group(vpc_id)
    if not alb_sg_id:
        return
    print()
    
    # Step 5: Configure SG rules
    print("Step 5: Configuring security group rules...")
    if not configure_sg_rules(web_sg_id, db_sg_id, alb_sg_id, bastion_sg_id):
        return
    print()
    
    # Step 6: Create NACL
    print("Step 6: Creating Network ACL...")
    subnet_id = input("Enter Subnet ID for NACL (or press Enter to skip): ").strip()
    if subnet_id:
        nacl_id = create_nacl(vpc_id, subnet_id)
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Security Groups & NACLs Setup Completed!")
    print("=" * 60)
    print()
    print("Security Groups Created:")
    print(f"  Bastion SG: {bastion_sg_id}")
    print(f"  Web SG: {web_sg_id}")
    print(f"  Database SG: {db_sg_id}")
    print(f"  ALB SG: {alb_sg_id}")
    print()

if __name__ == '__main__':
    main()
