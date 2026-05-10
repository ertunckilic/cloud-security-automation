# DAY 7: CloudTrail & CloudWatch Monitoring

## Overview

This day covers CloudTrail setup for comprehensive audit logging and CloudWatch alarms for real-time security monitoring.

## What We Did

### 1. CloudTrail Setup
- Enabled CloudTrail for all AWS regions
- Created S3 bucket for log storage
- Enabled log file validation
- Multi-region trail configuration

### 2. CloudWatch Monitoring
- Created CloudWatch log group
- Set up metric filters for security events
- Configured 6 critical security alarms
- SNS topic for alert notifications

### 3. Security Alarms
- Unauthorized API calls
- Root account usage
- IAM policy changes
- MFA device deactivation
- Security group changes
- S3 bucket policy changes

### 4. Log Analysis
- Python script to analyze CloudTrail logs
- Security event categorization
- Automated reporting

### 5. Infrastructure as Code
- Terraform configuration for CloudTrail
- Terraform configuration for CloudWatch
- Reusable and version-controlled

## Files

week-1/day7-cloudtrail-cloudwatch/
├── enable-cloudtrail.py
├── setup-cloudwatch-alarms.py
├── analyze-cloudtrail-logs.py
├── cloudtrail-cloudwatch-terraform.tf
└── README.md

## How to Use

### Step 1: Enable CloudTrail

cd ~/cloud-security-automation/week-1/day7-cloudtrail-cloudwatch
python3 enable-cloudtrail.py

### Step 2: Setup CloudWatch Alarms

python3 setup-cloudwatch-alarms.py

### Step 3: Analyze CloudTrail Logs

python3 analyze-cloudtrail-logs.py

### Step 4: Deploy with Terraform

terraform init
terraform plan
terraform apply

## CloudTrail Configuration

- Trail Name: cloud-security-audit-trail
- S3 Bucket: cloud-security-audit-logs
- Multi-Region: Enabled
- Log File Validation: Enabled
- Global Service Events: Enabled

## CloudWatch Alarms

1. SecurityAlert-UnauthorizedAPICalls
   - Triggers on unauthorized API attempts
   - Threshold: 1 event

2. SecurityAlert-RootAccountUsage
   - Triggers on root account activity
   - Threshold: 1 event

3. SecurityAlert-IAMPolicyChanges
   - Triggers on IAM policy modifications
   - Threshold: 1 event

4. SecurityAlert-MFADisable
   - Triggers on MFA device deactivation
   - Threshold: 1 event

5. SecurityAlert-SecurityGroupChanges
   - Triggers on security group modifications
   - Threshold: 1 event

6. SecurityAlert-S3BucketPolicyChanges
   - Triggers on S3 policy changes
   - Threshold: 1 event

## SNS Topic

Topic Name: cloud-security-alerts
Endpoint: Email (configurable)
Status: Subscription pending (check email for confirmation)

## Security Best Practices

DO:
- Enable CloudTrail for all regions
- Store logs in S3 with versioning
- Enable log file validation
- Set up SNS notifications
- Monitor root account usage
- Alert on IAM changes
- Review logs regularly

DON'T:
- Disable CloudTrail
- Delete CloudTrail logs
- Ignore security alarms
- Use weak SNS topic access
- Store logs without encryption
- Disable log file validation

## Compliance

- CloudTrail: Enabled for all regions
- Logs: Validated and stored in S3
- Alarms: 6 critical security alerts
- Monitoring: Real-time via CloudWatch
- Notifications: SNS email alerts

## AWS Services Used

- CloudTrail: Audit logging
- CloudWatch: Monitoring and alarms
- S3: Log storage
- SNS: Alert notifications
- IAM: Access control

## Python Dependencies

boto3
datetime
json
collections

## Terraform Resources

- aws_s3_bucket
- aws_s3_bucket_public_access_block
- aws_s3_bucket_versioning
- aws_s3_bucket_policy
- aws_cloudtrail
- aws_cloudwatch_log_group
- aws_cloudwatch_log_group_metric_filter
- aws_cloudwatch_metric_alarm
- aws_sns_topic

## Log Analysis Output

The analyze-cloudtrail-logs.py script provides:
- Total event count
- Top events by frequency
- Security event analysis
- Unauthorized access attempts
- Root account usage
- IAM changes
- MFA changes
- Security group changes
- S3 changes

## Troubleshooting

### CloudTrail not logging
- Check S3 bucket policy
- Verify CloudTrail is started
- Check IAM permissions

### Alarms not firing
- Verify metric filters
- Check log group name
- Confirm SNS topic subscription

### No email notifications
- Confirm SNS subscription
- Check spam folder
- Verify email address

## Next Steps (Week 2)

1. VPC and Network Security
2. Security Groups and NACLs
3. Advanced IAM Policies
4. KMS Encryption
5. Incident Response Automation

## Resources

- AWS CloudTrail: https://docs.aws.amazon.com/cloudtrail/
- CloudWatch: https://docs.aws.amazon.com/cloudwatch/
- Terraform AWS: https://registry.terraform.io/providers/hashicorp/aws/

## Author

- Created: 2026-05-10
- Status: Complete

DAY 7 COMPLETED SUCCESSFULLY!
