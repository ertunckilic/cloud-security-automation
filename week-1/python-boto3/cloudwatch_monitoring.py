#!/usr/bin/env python3
"""
Day 3: CloudWatch monitoring using Boto3
Learn: Monitor EC2 instances and create alarms
"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

def get_ec2_metrics(instance_id, metric_name='CPUUtilization', hours=1):
    """Get CloudWatch metrics for EC2 instance"""
    
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,  # 5 minutes
            Statistics=['Average', 'Maximum', 'Minimum']
        )
        
        datapoints = response.get('Datapoints', [])
        
        print(f"\n📊 CloudWatch Metrics: {instance_id}")
        print("-" * 60)
        print(f"Metric: {metric_name}")
        print(f"Time Range: {start_time} to {end_time}")
        print(f"Data Points: {len(datapoints)}\n")
        
        if datapoints:
            for dp in sorted(datapoints, key=lambda x: x['Timestamp']):
                print(f"  {dp['Timestamp']}")
                print(f"    Average: {dp.get('Average', 'N/A')}")
                print(f"    Maximum: {dp.get('Maximum', 'N/A')}")
                print(f"    Minimum: {dp.get('Minimum', 'N/A')}")
        else:
            print("  ℹ️  No data points available")
        
        return datapoints
    
    except ClientError as e:
        print(f"❌ Error getting metrics: {e}")
        return None

def list_cloudwatch_alarms():
    """List all CloudWatch alarms"""
    
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    
    try:
        response = cloudwatch.describe_alarms()
        alarms = response.get('MetricAlarms', [])
        
        print("\n" + "="*80)
        print("CLOUDWATCH ALARMS".center(80))
        print("="*80 + "\n")
        
        if not alarms:
            print("❌ No alarms found")
        else:
            print(f"✅ Found {len(alarms)} alarm(s)\n")
            for alarm in alarms:
                print(f"  • {alarm['AlarmName']}")
                print(f"    State: {alarm['StateValue']}")
                print(f"    Metric: {alarm['MetricName']}")
                print()
        
        return alarms
    
    except ClientError as e:
        print(f"❌ Error: {e}")
        return None

def create_cpu_alarm(instance_id, threshold=80):
    """Create CPU utilization alarm for instance"""
    
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    alarm_name = f"cpu-alarm-{instance_id}"
    
    try:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistic='Average',
            Period=300,
            EvaluationPeriods=2,
            Threshold=threshold,
            ComparisonOperator='GreaterThanThreshold',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                }
            ],
            AlarmDescription=f'Alert when CPU > {threshold}% for instance {instance_id}'
        )
        
        print(f"✅ Alarm created: {alarm_name}")
        print(f"   Threshold: {threshold}%")
        return True
    
    except ClientError as e:
        print(f"❌ Error creating alarm: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("CLOUDWATCH MONITORING".center(80))
    print("="*80 + "\n")
    
    # List all alarms
    list_cloudwatch_alarms()
    
    print("\n✅ CloudWatch monitoring initialized")
    print("Usage examples:")
    print("  get_ec2_metrics('i-xxxxx')")
    print("  create_cpu_alarm('i-xxxxx', threshold=75)")
