import boto3
import json
from datetime import datetime

# Initialize client
ec2 = boto3.client('ec2')

# Configuration
VPC_CIDR = '10.0.0.0/16'
PUBLIC_SUBNET_CIDR = '10.0.1.0/24'
PRIVATE_SUBNET_CIDR = '10.0.2.0/24'
VPC_NAME = 'cloud-security-vpc'
REGION = ec2.meta.region_name

def create_vpc():
    """Create VPC"""
    try:
        response = ec2.create_vpc(CidrBlock=VPC_CIDR)
        vpc_id = response['Vpc']['VpcId']
        
        # Tag VPC
        ec2.create_tags(
            Resources=[vpc_id],
            Tags=[
                {'Key': 'Name', 'Value': VPC_NAME},
                {'Key': 'Environment', 'Value': 'production'},
                {'Key': 'Purpose', 'Value': 'Cloud-Security'}
            ]
        )
        
        print(f"✅ VPC created: {vpc_id}")
        print(f"   CIDR: {VPC_CIDR}")
        return vpc_id
    except Exception as e:
        print(f"❌ Error creating VPC: {e}")
        return None

def create_public_subnet(vpc_id):
    """Create public subnet"""
    try:
        response = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=PUBLIC_SUBNET_CIDR,
            AvailabilityZone=f'{REGION}a'
        )
        subnet_id = response['Subnet']['SubnetId']
        
        # Tag subnet
        ec2.create_tags(
            Resources=[subnet_id],
            Tags=[
                {'Key': 'Name', 'Value': 'public-subnet-1a'},
                {'Key': 'Type', 'Value': 'Public'}
            ]
        )
        
        print(f"✅ Public subnet created: {subnet_id}")
        print(f"   CIDR: {PUBLIC_SUBNET_CIDR}")
        return subnet_id
    except Exception as e:
        print(f"❌ Error creating public subnet: {e}")
        return None

def create_private_subnet(vpc_id):
    """Create private subnet"""
    try:
        response = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=PRIVATE_SUBNET_CIDR,
            AvailabilityZone=f'{REGION}b'
        )
        subnet_id = response['Subnet']['SubnetId']
        
        # Tag subnet
        ec2.create_tags(
            Resources=[subnet_id],
            Tags=[
                {'Key': 'Name', 'Value': 'private-subnet-1b'},
                {'Key': 'Type', 'Value': 'Private'}
            ]
        )
        
        print(f"✅ Private subnet created: {subnet_id}")
        print(f"   CIDR: {PRIVATE_SUBNET_CIDR}")
        return subnet_id
    except Exception as e:
        print(f"❌ Error creating private subnet: {e}")
        return None

def create_internet_gateway(vpc_id):
    """Create Internet Gateway"""
    try:
        response = ec2.create_internet_gateway()
        igw_id = response['InternetGateway']['InternetGatewayId']
        
        # Tag IGW
        ec2.create_tags(
            Resources=[igw_id],
            Tags=[
                {'Key': 'Name', 'Value': 'cloud-security-igw'},
                {'Key': 'Purpose', 'Value': 'Internet-Access'}
            ]
        )
        
        # Attach to VPC
        ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
        
        print(f"✅ Internet Gateway created: {igw_id}")
        return igw_id
    except Exception as e:
        print(f"❌ Error creating Internet Gateway: {e}")
        return None

def create_route_table(vpc_id, is_public=True):
    """Create route table"""
    try:
        response = ec2.create_route_table(VpcId=vpc_id)
        rt_id = response['RouteTable']['RouteTableId']
        
        # Tag route table
        rt_type = 'Public' if is_public else 'Private'
        ec2.create_tags(
            Resources=[rt_id],
            Tags=[
                {'Key': 'Name', 'Value': f'{rt_type}-RouteTable'},
                {'Key': 'Type', 'Value': rt_type}
            ]
        )
        
        print(f"✅ {'Public' if is_public else 'Private'} route table created: {rt_id}")
        return rt_id
    except Exception as e:
        print(f"❌ Error creating route table: {e}")
        return None

def add_igw_route(rt_id, igw_id):
    """Add Internet Gateway route to public route table"""
    try:
        ec2.create_route(
            RouteTableId=rt_id,
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id
        )
        print(f"✅ IGW route added to route table")
        return True
    except Exception as e:
        print(f"❌ Error adding IGW route: {e}")
        return False

def associate_subnet_to_rt(subnet_id, rt_id):
    """Associate subnet to route table"""
    try:
        ec2.associate_route_table(
            RouteTableId=rt_id,
            SubnetId=subnet_id
        )
        print(f"✅ Subnet associated to route table")
        return True
    except Exception as e:
        print(f"❌ Error associating subnet: {e}")
        return False

def create_security_group(vpc_id):
    """Create security group"""
    try:
        response = ec2.create_security_group(
            GroupName='cloud-security-sg',
            Description='Security group for cloud security infrastructure',
            VpcId=vpc_id
        )
        sg_id = response['GroupId']
        
        # Tag security group
        ec2.create_tags(
            Resources=[sg_id],
            Tags=[
                {'Key': 'Name', 'Value': 'cloud-security-sg'},
                {'Key': 'Purpose', 'Value': 'Main-SG'}
            ]
        )
        
        # Add inbound rules
        # SSH
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'SSH'}]
                }
            ]
        )
        
        # HTTPS
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
        
        # HTTP
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
        
        print(f"✅ Security group created: {sg_id}")
        print(f"   Inbound rules: SSH (22), HTTP (80), HTTPS (443)")
        return sg_id
    except Exception as e:
        print(f"❌ Error creating security group: {e}")
        return None

def enable_vpc_flow_logs(vpc_id):
    """Enable VPC Flow Logs"""
    try:
        # Create CloudWatch log group first
        logs = boto3.client('logs')
        log_group = '/aws/vpc/flowlogs'
        
        try:
            logs.create_log_group(logGroupName=log_group)
            print(f"✅ CloudWatch log group created: {log_group}")
        except logs.exceptions.ResourceAlreadyExistsException:
            print(f"✅ CloudWatch log group exists: {log_group}")
        
        # Create IAM role for VPC Flow Logs
        iam = boto3.client('iam')
        role_name = 'vpc-flow-logs-role'
        
        try:
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "vpc-flow-logs.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Role for VPC Flow Logs'
            )
            
            # Attach policy
            iam.put_role_policy(
                RoleName=role_name,
                PolicyName='vpc-flow-logs-policy',
                PolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                                "logs:DescribeLogGroups",
                                "logs:DescribeLogStreams"
                            ],
                            "Resource": "*"
                        }
                    ]
                })
            )
            print(f"✅ IAM role created: {role_name}")
        except iam.exceptions.EntityAlreadyExistsException:
            print(f"✅ IAM role exists: {role_name}")
        
        # Get role ARN
        role_response = iam.get_role(RoleName=role_name)
        role_arn = role_response['Role']['Arn']
        
        # Create VPC Flow Logs
        ec2_client = boto3.client('ec2')
        response = ec2_client.create_flow_logs(
            ResourceType='VPC',
            ResourceIds=[vpc_id],
            TrafficType='ALL',
            LogDestinationType='cloud-watch-logs',
            LogGroupName=log_group,
            DeliverLogsPermissionIam=role_arn
        )
        
        print(f"✅ VPC Flow Logs enabled")
        return True
    except Exception as e:
        print(f"❌ Error enabling VPC Flow Logs: {e}")
        return False

def main():
    print("=" * 60)
    print("AWS VPC Setup")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print(f"Region: {REGION}")
    print(f"VPC CIDR: {VPC_CIDR}")
    print()
    
    # Step 1: Create VPC
    print("Step 1: Creating VPC...")
    vpc_id = create_vpc()
    if not vpc_id:
        print("Failed to create VPC. Exiting.")
        return
    print()
    
    # Step 2: Create Internet Gateway
    print("Step 2: Creating Internet Gateway...")
    igw_id = create_internet_gateway(vpc_id)
    if not igw_id:
        print("Failed to create Internet Gateway. Exiting.")
        return
    print()
    
    # Step 3: Create Public Subnet
    print("Step 3: Creating public subnet...")
    public_subnet_id = create_public_subnet(vpc_id)
    if not public_subnet_id:
        print("Failed to create public subnet. Exiting.")
        return
    print()
    
    # Step 4: Create Private Subnet
    print("Step 4: Creating private subnet...")
    private_subnet_id = create_private_subnet(vpc_id)
    if not private_subnet_id:
        print("Failed to create private subnet. Exiting.")
        return
    print()
    
    # Step 5: Create Public Route Table
    print("Step 5: Creating public route table...")
    public_rt_id = create_route_table(vpc_id, is_public=True)
    if not public_rt_id:
        print("Failed to create public route table. Exiting.")
        return
    print()
    
    # Step 6: Add IGW route to public route table
    print("Step 6: Adding Internet Gateway route...")
    if not add_igw_route(public_rt_id, igw_id):
        print("Failed to add IGW route. Exiting.")
        return
    print()
    
    # Step 7: Associate public subnet to public route table
    print("Step 7: Associating public subnet to route table...")
    if not associate_subnet_to_rt(public_subnet_id, public_rt_id):
        print("Failed to associate subnet. Exiting.")
        return
    print()
    
    # Step 8: Create Private Route Table
    print("Step 8: Creating private route table...")
    private_rt_id = create_route_table(vpc_id, is_public=False)
    if not private_rt_id:
        print("Failed to create private route table. Exiting.")
        return
    print()
    
    # Step 9: Associate private subnet to private route table
    print("Step 9: Associating private subnet to route table...")
    if not associate_subnet_to_rt(private_subnet_id, private_rt_id):
        print("Failed to associate subnet. Exiting.")
        return
    print()
    
    # Step 10: Create Security Group
    print("Step 10: Creating security group...")
    sg_id = create_security_group(vpc_id)
    if not sg_id:
        print("Failed to create security group. Exiting.")
        return
    print()
    
    # Step 11: Enable VPC Flow Logs
    print("Step 11: Enabling VPC Flow Logs...")
    enable_vpc_flow_logs(vpc_id)
    print()
    
    # Summary
    print("=" * 60)
    print("✅ VPC Setup Completed Successfully!")
    print("=" * 60)
    print()
    print("VPC Infrastructure Summary:")
    print(f"  VPC ID: {vpc_id}")
    print(f"  VPC CIDR: {VPC_CIDR}")
    print(f"  Internet Gateway: {igw_id}")
    print(f"  Public Subnet: {public_subnet_id}")
    print(f"  Private Subnet: {private_subnet_id}")
    print(f"  Public Route Table: {public_rt_id}")
    print(f"  Private Route Table: {private_rt_id}")
    print(f"  Security Group: {sg_id}")
    print()

if __name__ == '__main__':
    main()
