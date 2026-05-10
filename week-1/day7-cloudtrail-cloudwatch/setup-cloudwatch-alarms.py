import boto3
import json
from datetime import datetime

# Initialize clients
cloudwatch = boto3.client('cloudwatch')
logs = boto3.client('logs')
sns = boto3.client('sns')

LOG_GROUP_NAME = '/aws/cloudtrail/security-audit'
ALARM_PREFIX = 'SecurityAlert'
SNS_TOPIC_NAME = 'cloud-security-alerts'
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']

def create_sns_topic():
    """Create SNS topic for alerts"""
    try:
        response = sns.create_topic(Name=SNS_TOPIC_NAME)
        topic_arn = response['TopicArn']
        print(f"✅ SNS topic created: {SNS_TOPIC_NAME}")
        print(f"   ARN: {topic_arn}")
        return topic_arn
    except Exception as e:
        print(f"❌ Error creating SNS topic: {e}")
        return None

def subscribe_to_topic(topic_arn, email):
    """Subscribe email to SNS topic"""
    try:
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email
        )
        print(f"✅ Email subscription pending (check inbox for confirmation)")
        return response['SubscriptionArn']
    except Exception as e:
        print(f"❌ Error subscribing to topic: {e}")
        return None

def create_log_group():
    """Create CloudWatch log group"""
    try:
        logs.create_log_group(logGroupName=LOG_GROUP_NAME)
        print(f"✅ Log group '{LOG_GROUP_NAME}' created")
        return True
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"✅ Log group '{LOG_GROUP_NAME}' already exists")
        return True
    except Exception as e:
        print(f"❌ Error creating log group: {e}")
        return False

def create_metric_filter(filter_name, pattern, metric_name, namespace):
    """Create CloudWatch metric filter"""
    try:
        logs.put_metric_filter(
            logGroupName=LOG_GROUP_NAME,
            filterName=filter_name,
            filterPattern=pattern,
            metricTransformations=[
                {
                    'metricName': metric_name,
                    'metricNamespace': namespace,
                    'metricValue': '1',
                    'defaultValue': 0
                }
            ]
        )
        print(f"✅ Metric filter created: {filter_name}")
        return True
    except Exception as e:
        print(f"❌ Error creating metric filter: {e}")
        return False

def create_alarm(alarm_name, metric_name, namespace, threshold, comparison, description, topic_arn):
    """Create CloudWatch alarm"""
    try:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription=description,
            MetricName=metric_name,
            Namespace=namespace,
            Statistic='Sum',
            Period=300,
            EvaluationPeriods=1,
            Threshold=threshold,
            ComparisonOperator=comparison,
            AlarmActions=[topic_arn],
            TreatMissingData='notBreaching'
        )
        print(f"✅ Alarm created: {alarm_name}")
        return True
    except Exception as e:
        print(f"❌ Error creating alarm: {e}")
        return False

def main():
    print("=" * 60)
    print("AWS CloudWatch Alarms Setup")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print(f"Account ID: {ACCOUNT_ID}")
    print(f"Log Group: {LOG_GROUP_NAME}")
    print(f"SNS Topic: {SNS_TOPIC_NAME}")
    print()
    
    # Step 1: Create SNS topic
    print("Step 1: Creating SNS topic for alerts...")
    topic_arn = create_sns_topic()
    if not topic_arn:
        print("Failed to create SNS topic. Exiting.")
        return
    print()
    
    # Step 2: Subscribe email
    print("Step 2: Subscribing to alerts...")
    email = input("Enter your email for alerts (or press Enter to skip): ").strip()
    if email:
        subscribe_to_topic(topic_arn, email)
        print()
    
    # Step 3: Create log group
    print("Step 3: Creating CloudWatch log group...")
    if not create_log_group():
        print("Failed to create log group. Exiting.")
        return
    print()
    
    # Step 4: Create metric filters and alarms
    print("Step 4: Creating metric filters and alarms...")
    print()
    
    alarms = [
        {
            'filter_name': 'UnauthorizedAPICallsMetricFilter',
            'pattern': '{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }',
            'metric_name': 'UnauthorizedAPICallsMetric',
            'alarm_name': f'{ALARM_PREFIX}-UnauthorizedAPICalls',
            'description': 'Alert on unauthorized API calls'
        },
        {
            'filter_name': 'RootAccountUsageMetricFilter',
            'pattern': '{ $.userIdentity.type = "Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != "AwsServiceEvent" }',
            'metric_name': 'RootAccountUsageMetric',
            'alarm_name': f'{ALARM_PREFIX}-RootAccountUsage',
            'description': 'Alert on root account usage'
        },
        {
            'filter_name': 'IAMPolicyChangesMetricFilter',
            'pattern': '{ ($.eventName = DeleteGroupPolicy) || ($.eventName = DeleteRolePolicy) || ($.eventName = DeleteUserPolicy) || ($.eventName = PutGroupPolicy) || ($.eventName = PutRolePolicy) || ($.eventName = PutUserPolicy) || ($.eventName = CreatePolicy) || ($.eventName = DeletePolicy) || ($.eventName = CreatePolicyVersion) || ($.eventName = DeletePolicyVersion) || ($.eventName = AttachRolePolicy) || ($.eventName = DetachRolePolicy) || ($.eventName = AttachUserPolicy) || ($.eventName = DetachUserPolicy) || ($.eventName = AttachGroupPolicy) || ($.eventName = DetachGroupPolicy) }',
            'metric_name': 'IAMPolicyChangesMetric',
            'alarm_name': f'{ALARM_PREFIX}-IAMPolicyChanges',
            'description': 'Alert on IAM policy changes'
        },
        {
            'filter_name': 'MFADisableMetricFilter',
            'pattern': '{ ($.eventName = DeactivateMFADevice) || ($.eventName = DeleteVirtualMFADevice) }',
            'metric_name': 'MFADisableMetric',
            'alarm_name': f'{ALARM_PREFIX}-MFADisable',
            'description': 'Alert on MFA device deactivation'
        },
        {
            'filter_name': 'SecurityGroupChangesMetricFilter',
            'pattern': '{ ($.eventName = AuthorizeSecurityGroupIngress) || ($.eventName = AuthorizeSecurityGroupEgress) || ($.eventName = RevokeSecurityGroupIngress) || ($.eventName = RevokeSecurityGroupEgress) || ($.eventName = CreateSecurityGroup) || ($.eventName = DeleteSecurityGroup) }',
            'metric_name': 'SecurityGroupChangesMetric',
            'alarm_name': f'{ALARM_PREFIX}-SecurityGroupChanges',
            'description': 'Alert on security group changes'
        },
        {
            'filter_name': 'S3BucketPolicyChangesMetricFilter',
            'pattern': '{ ($.eventName = PutBucketPolicy) || ($.eventName = DeleteBucketPolicy) }',
            'metric_name': 'S3BucketPolicyChangesMetric',
            'alarm_name': f'{ALARM_PREFIX}-S3BucketPolicyChanges',
            'description': 'Alert on S3 bucket policy changes'
        }
    ]
    
    for alarm in alarms:
        print(f"Creating filter: {alarm['filter_name']}")
        create_metric_filter(
            alarm['filter_name'],
            alarm['pattern'],
            alarm['metric_name'],
            'CloudTrailMetrics'
        )
        print(f"Creating alarm: {alarm['alarm_name']}")
        create_alarm(
            alarm['alarm_name'],
            alarm['metric_name'],
            'CloudTrailMetrics',
            threshold=1,
            comparison='GreaterThanOrEqualToThreshold',
            description=alarm['description'],
            topic_arn=topic_arn
        )
        print()
    
    print("=" * 60)
    print("✅ CloudWatch alarms setup completed successfully!")
    print("=" * 60)
    print()
    print("Active Alarms:")
    for alarm in alarms:
        print(f"  - {alarm['alarm_name']}")

if __name__ == '__main__':
    main()
