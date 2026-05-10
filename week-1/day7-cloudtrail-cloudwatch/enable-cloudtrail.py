import boto3
import json
from datetime import datetime

# Initialize clients
cloudtrail = boto3.client('cloudtrail')
s3 = boto3.client('s3')
iam = boto3.client('iam')

TRAIL_NAME = 'cloud-security-audit-trail'
S3_BUCKET = 'cloud-security-audit-logs'
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']

def create_s3_bucket():
    """Create S3 bucket for CloudTrail logs"""
    try:
        s3.head_bucket(Bucket=S3_BUCKET)
        print(f"✅ S3 bucket '{S3_BUCKET}' already exists")
        return True
    except:
        try:
            s3.create_bucket(
                Bucket=S3_BUCKET,
                CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'}
            )
            print(f"✅ Created S3 bucket '{S3_BUCKET}'")
            
            # Block public access
            s3.put_public_access_block(
                Bucket=S3_BUCKET,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            print(f"✅ Blocked public access for '{S3_BUCKET}'")
            return True
        except Exception as e:
            print(f"❌ Error creating S3 bucket: {e}")
            return False

def create_cloudtrail_policy():
    """Create IAM policy for CloudTrail"""
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{S3_BUCKET}"
            },
            {
                "Sid": "AWSCloudTrailWrite",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{S3_BUCKET}/AWSLogs/{ACCOUNT_ID}/*",
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                }
            }
        ]
    }
    
    try:
        s3.put_bucket_policy(
            Bucket=S3_BUCKET,
            Policy=json.dumps(policy_document)
        )
        print(f"✅ CloudTrail bucket policy attached")
        return True
    except Exception as e:
        print(f"❌ Error setting bucket policy: {e}")
        return False

def create_cloudtrail():
    """Create CloudTrail"""
    try:
        response = cloudtrail.create_trail(
            Name=TRAIL_NAME,
            S3BucketName=S3_BUCKET,
            IncludeGlobalServiceEvents=True,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=True,
            IsOrganizationTrail=False
        )
        print(f"✅ CloudTrail '{TRAIL_NAME}' created")
        print(f"   Trail ARN: {response['TrailARN']}")
        return True
    except cloudtrail.exceptions.TrailAlreadyExistsException:
        print(f"✅ CloudTrail '{TRAIL_NAME}' already exists")
        return True
    except Exception as e:
        print(f"❌ Error creating CloudTrail: {e}")
        return False

def start_cloudtrail():
    """Start CloudTrail logging"""
    try:
        cloudtrail.start_logging(Name=TRAIL_NAME)
        print(f"✅ CloudTrail logging started")
        return True
    except Exception as e:
        print(f"❌ Error starting logging: {e}")
        return False

def get_trail_status():
    """Get CloudTrail status"""
    try:
        response = cloudtrail.get_trail_status(Name=TRAIL_NAME)
        return response
    except Exception as e:
        print(f"❌ Error getting trail status: {e}")
        return None

def main():
    print("=" * 60)
    print("AWS CloudTrail Setup")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print(f"Account ID: {ACCOUNT_ID}")
    print(f"Trail Name: {TRAIL_NAME}")
    print(f"S3 Bucket: {S3_BUCKET}")
    print()
    
    # Step 1: Create S3 bucket
    print("Step 1: Creating S3 bucket...")
    if not create_s3_bucket():
        print("Failed to create S3 bucket. Exiting.")
        return
    print()
    
    # Step 2: Create CloudTrail policy
    print("Step 2: Setting CloudTrail bucket policy...")
    if not create_cloudtrail_policy():
        print("Failed to set bucket policy. Exiting.")
        return
    print()
    
    # Step 3: Create CloudTrail
    print("Step 3: Creating CloudTrail...")
    if not create_cloudtrail():
        print("Failed to create CloudTrail. Exiting.")
        return
    print()
    
    # Step 4: Start logging
    print("Step 4: Starting CloudTrail logging...")
    if not start_cloudtrail():
        print("Failed to start logging. Exiting.")
        return
    print()
    
    # Step 5: Get status
    print("Step 5: CloudTrail Status")
    status = get_trail_status()
    if status:
        print(f"   IsLogging: {status['IsLogging']}")
        print(f"   LatestDeliveryTime: {status.get('LatestDeliveryTime', 'N/A')}")
        print(f"   LatestDeliveryAttemptTime: {status.get('LatestDeliveryAttemptTime', 'N/A')}")
    print()
    
    print("=" * 60)
    print("✅ CloudTrail setup completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
