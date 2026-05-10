#!/usr/bin/env python3
"""
MFA Status Checker
Checks which IAM users have MFA enabled
"""

import boto3
import json
from datetime import datetime

def check_mfa_status():
    """Check MFA status for all IAM users"""
    
    iam = boto3.client('iam')
    
    print("=" * 60)
    print("AWS MFA Status Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Get all users
        response = iam.list_users()
        users = response['Users']
        
        mfa_enabled = 0
        mfa_disabled = 0
        
        print(f"\nTotal IAM Users: {len(users)}\n")
        print(f"{'Username':<20} {'MFA Status':<15} {'Devices':<10}")
        print("-" * 60)
        
        for user in users:
            username = user['UserName']
            
            # Get MFA devices
            mfa_response = iam.list_mfa_devices(UserName=username)
            mfa_devices = mfa_response['MFADevices']
            
            if mfa_devices:
                status = "✅ ENABLED"
                device_count = len(mfa_devices)
                mfa_enabled += 1
            else:
                status = "❌ DISABLED"
                device_count = 0
                mfa_disabled += 1
            
            print(f"{username:<20} {status:<15} {device_count:<10}")
        
        print("-" * 60)
        print(f"\nSummary:")
        print(f"  MFA Enabled:  {mfa_enabled} users")
        print(f"  MFA Disabled: {mfa_disabled} users")
        print(f"  Compliance:   {(mfa_enabled/len(users)*100):.1f}%")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have AWS credentials configured")

if __name__ == "__main__":
    check_mfa_status()
