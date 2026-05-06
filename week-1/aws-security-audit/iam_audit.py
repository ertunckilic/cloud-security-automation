#!/usr/bin/env python3
"""
IAM Audit Script - Security Posture Analysis
"""

import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

class IAMAudit:
    def __init__(self):
        self.iam = boto3.client('iam')
        self.sts = boto3.client('sts')
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'account_id': None,
            'current_user': None,
            'findings': {
                'critical': [],
                'high': [],
            },
            'user_details': {},
            'attached_policies': [],
            'access_keys': [],
            'mfa_devices': [],
        }

    def get_account_info(self):
        """Get current account and user information"""
        try:
            identity = self.sts.get_caller_identity()
            self.report['account_id'] = identity['Account']
            self.report['current_user'] = identity['Arn']
        except ClientError as e:
            self.report['findings']['critical'].append(
                f"Failed to get identity: {e.response['Error']['Message']}"
            )

    def audit_user(self, username):
        """Audit specific IAM user"""
        try:
            user = self.iam.get_user(UserName=username)
            self.report['user_details'] = {
                'UserName': user['User']['UserName'],
                'UserId': user['User']['UserId'],
                'Arn': user['User']['Arn'],
                'CreateDate': str(user['User']['CreateDate']),
            }
        except ClientError as e:
            self.report['findings']['critical'].append(
                f"Failed to get user {username}: {e.response['Error']['Message']}"
            )

    def audit_attached_policies(self, username):
        """Get attached managed policies"""
        try:
            policies = self.iam.list_attached_user_policies(UserName=username)
            self.report['attached_policies'] = [
                {
                    'PolicyName': p['PolicyName'],
                    'PolicyArn': p['PolicyArn']
                }
                for p in policies['AttachedPolicies']
            ]
        except ClientError as e:
            self.report['findings']['high'].append(
                f"Failed to list attached policies: {e.response['Error']['Message']}"
            )

    def audit_access_keys(self, username):
        """Audit access keys"""
        try:
            keys = self.iam.list_access_keys(UserName=username)
            for key in keys['AccessKeyMetadata']:
                key_age_days = (datetime.now(key['CreateDate'].tzinfo) - key['CreateDate']).days
                self.report['access_keys'].append({
                    'AccessKeyId': key['AccessKeyId'][:10] + '***',
                    'Status': key['Status'],
                    'CreateDate': str(key['CreateDate']),
                    'AgeInDays': key_age_days
                })
        except ClientError as e:
            self.report['findings']['high'].append(
                f"Failed to list access keys: {e.response['Error']['Message']}"
            )

    def audit_mfa(self, username):
        """Check MFA status"""
        try:
            mfa_devices = self.iam.list_mfa_devices(UserName=username)
            self.report['mfa_devices'] = [
                {
                    'SerialNumber': d['SerialNumber'],
                    'EnableDate': str(d['EnableDate'])
                }
                for d in mfa_devices['MFADevices']
            ]
        except ClientError as e:
            self.report['findings']['high'].append(
                f"Failed to check MFA: {e.response['Error']['Message']}"
            )

    def run_full_audit(self, username):
        """Execute complete audit"""
        print(f"🔍 Starting IAM Audit for user: {username}\n")
        self.get_account_info()
        self.audit_user(username)
        self.audit_attached_policies(username)
        self.audit_access_keys(username)
        self.audit_mfa(username)
        return self.report

    def print_report(self):
        """Pretty-print the audit report"""
        print("\n" + "="*70)
        print("AWS IAM SECURITY AUDIT REPORT")
        print("="*70)
        print(f"Timestamp: {self.report['timestamp']}")
        print(f"Account ID: {self.report['account_id']}")
        
        print("\n--- USER DETAILS ---")
        for key, value in self.report['user_details'].items():
            print(f"  {key}: {value}")
        
        print("\n--- ATTACHED POLICIES ---")
        if self.report['attached_policies']:
            for policy in self.report['attached_policies']:
                print(f"  • {policy['PolicyName']}")
        else:
            print("  None")
        
        print("\n--- ACCESS KEYS ---")
        if self.report['access_keys']:
            for key in self.report['access_keys']:
                print(f"  • {key['AccessKeyId']} (Age: {key['AgeInDays']} days)")
        else:
            print("  None")
        
        print("\n--- MFA DEVICES ---")
        if self.report['mfa_devices']:
            for device in self.report['mfa_devices']:
                print(f"  • MFA Enabled")
        else:
            print("  ⚠️  NO MFA")
        
        print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else 'ertunckilic-dev'
    
    audit = IAMAudit()
    audit.run_full_audit(username)
    audit.print_report()
