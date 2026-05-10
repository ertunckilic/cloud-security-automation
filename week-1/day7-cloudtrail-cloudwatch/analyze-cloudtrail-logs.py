import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Initialize clients
cloudtrail = boto3.client('cloudtrail')
s3 = boto3.client('s3')

S3_BUCKET = 'cloud-security-audit-logs'
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']

def get_recent_events(days=1):
    """Get recent CloudTrail events"""
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        events = []
        paginator = cloudtrail.get_paginator('lookup_events')
        
        page_iterator = paginator.paginate(
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50
        )
        
        for page in page_iterator:
            events.extend(page.get('Events', []))
        
        return events
    except Exception as e:
        print(f"❌ Error getting events: {e}")
        return []

def categorize_events(events):
    """Categorize events by type"""
    categories = defaultdict(list)
    
    for event in events:
        event_name = event.get('EventName', 'Unknown')
        categories[event_name].append(event)
    
    return categories

def analyze_security_events(events):
    """Analyze security-relevant events"""
    security_events = {
        'unauthorized_access': [],
        'iam_changes': [],
        'mfa_changes': [],
        'security_group_changes': [],
        'root_usage': [],
        's3_changes': []
    }
    
    for event in events:
        event_name = event.get('EventName', '')
        cloud_trail_event = json.loads(event.get('CloudTrailEvent', '{}'))
        error_code = cloud_trail_event.get('errorCode', '')
        user_identity = cloud_trail_event.get('userIdentity', {})
        
        # Unauthorized access
        if 'Unauthorized' in error_code or 'AccessDenied' in error_code:
            security_events['unauthorized_access'].append(event)
        
        # IAM changes
        if event_name.startswith(('PutUser', 'CreateUser', 'DeleteUser', 'AttachUser', 'DetachUser')):
            security_events['iam_changes'].append(event)
        
        # MFA changes
        if 'MFA' in event_name or 'MFA' in event_name:
            security_events['mfa_changes'].append(event)
        
        # Security group changes
        if 'SecurityGroup' in event_name:
            security_events['security_group_changes'].append(event)
        
        # Root account usage
        if user_identity.get('type') == 'Root':
            security_events['root_usage'].append(event)
        
        # S3 changes
        if event_name.startswith(('PutBucketPolicy', 'DeleteBucketPolicy', 'PutObject', 'DeleteObject')):
            security_events['s3_changes'].append(event)
    
    return security_events

def print_event_summary(events):
    """Print summary of events"""
    print()
    print("=" * 60)
    print("CloudTrail Events Summary")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    if not events:
        print("No events found in the last 24 hours")
        return
    
    # Event count
    print(f"Total Events: {len(events)}")
    print()
    
    # Top events
    categories = categorize_events(events)
    print("Top Events:")
    for event_name, event_list in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"  {event_name}: {len(event_list)}")
    print()

def print_security_analysis(security_events):
    """Print security analysis"""
    print("=" * 60)
    print("Security Analysis")
    print("=" * 60)
    print()
    
    total_issues = sum(len(v) for v in security_events.values())
    
    if total_issues == 0:
        print("✅ No security issues detected")
        print()
        return
    
    print(f"⚠️  Total Security Events: {total_issues}")
    print()
    
    if security_events['unauthorized_access']:
        print(f"❌ Unauthorized Access Attempts: {len(security_events['unauthorized_access'])}")
        for event in security_events['unauthorized_access'][:3]:
            print(f"   - {event['EventName']} by {event['Username']} at {event['EventTime']}")
        print()
    
    if security_events['root_usage']:
        print(f"❌ Root Account Usage: {len(security_events['root_usage'])}")
        for event in security_events['root_usage'][:3]:
            print(f"   - {event['EventName']} at {event['EventTime']}")
        print()
    
    if security_events['iam_changes']:
        print(f"⚠️  IAM Changes: {len(security_events['iam_changes'])}")
        for event in security_events['iam_changes'][:3]:
            print(f"   - {event['EventName']} by {event['Username']} at {event['EventTime']}")
        print()
    
    if security_events['mfa_changes']:
        print(f"⚠️  MFA Changes: {len(security_events['mfa_changes'])}")
        for event in security_events['mfa_changes'][:3]:
            print(f"   - {event['EventName']} by {event['Username']} at {event['EventTime']}")
        print()
    
    if security_events['security_group_changes']:
        print(f"⚠️  Security Group Changes: {len(security_events['security_group_changes'])}")
        for event in security_events['security_group_changes'][:3]:
            print(f"   - {event['EventName']} by {event['Username']} at {event['EventTime']}")
        print()
    
    if security_events['s3_changes']:
        print(f"⚠️  S3 Changes: {len(security_events['s3_changes'])}")
        for event in security_events['s3_changes'][:3]:
            print(f"   - {event['EventName']} by {event['Username']} at {event['EventTime']}")
        print()

def main():
    print()
    print("Fetching CloudTrail events (last 24 hours)...")
    print()
    
    # Get events
    events = get_recent_events(days=1)
    
    # Print summary
    print_event_summary(events)
    
    # Analyze security
    security_events = analyze_security_events(events)
    print_security_analysis(security_events)
    
    print("=" * 60)
    print("Analysis Complete")
    print("=" * 60)

if __name__ == '__main__':
    main()
