# CloudTrail and CloudWatch Configuration
# This enables comprehensive audit logging and monitoring

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "trail_name" {
  description = "CloudTrail name"
  type        = string
  default     = "cloud-security-audit-trail"
}

variable "s3_bucket_name" {
  description = "S3 bucket for CloudTrail logs"
  type        = string
  default     = "cloud-security-audit-logs"
}

# S3 Bucket for CloudTrail logs
resource "aws_s3_bucket" "cloudtrail_logs" {
  bucket = var.s3_bucket_name

  tags = {
    Name        = "CloudTrail-Logs"
    Environment = var.environment
    Purpose     = "Audit-Logging"
  }
}

# Block public access to S3 bucket
resource "aws_s3_bucket_public_access_block" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 bucket versioning
resource "aws_s3_bucket_versioning" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

# S3 bucket policy for CloudTrail
resource "aws_s3_bucket_policy" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.cloudtrail_logs.arn
      },
      {
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.cloudtrail_logs.arn}/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

# CloudTrail
resource "aws_cloudtrail" "main" {
  name                          = var.trail_name
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  depends_on                    = [aws_s3_bucket_policy.cloudtrail_logs]

  tags = {
    Name        = "Cloud-Security-Audit-Trail"
    Environment = var.environment
  }
}

# Start CloudTrail logging
resource "aws_cloudtrail_status" "main" {
  depends_on       = [aws_cloudtrail.main]
  is_multi_region_trail = true
  trail_name       = aws_cloudtrail.main.name
  is_logging       = true
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "cloudtrail_logs" {
  name              = "/aws/cloudtrail/security-audit"
  retention_in_days = 30

  tags = {
    Name        = "CloudTrail-Logs"
    Environment = var.environment
  }
}

# SNS Topic for alerts
resource "aws_sns_topic" "security_alerts" {
  name = "cloud-security-alerts"

  tags = {
    Name        = "Security-Alerts"
    Environment = var.environment
  }
}

# Metric Filter - Unauthorized API Calls
resource "aws_cloudwatch_log_group_metric_filter" "unauthorized_api_calls" {
  name           = "UnauthorizedAPICallsMetricFilter"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name
  filter_pattern = "{ ($.errorCode = \"*UnauthorizedOperation\") || ($.errorCode = \"AccessDenied*\") }"

  metric_transformation {
    name      = "UnauthorizedAPICallsMetric"
    namespace = "CloudTrailMetrics"
    value     = "1"
  }
}

# Alarm - Unauthorized API Calls
resource "aws_cloudwatch_metric_alarm" "unauthorized_api_calls" {
  alarm_name          = "SecurityAlert-UnauthorizedAPICalls"
  alarm_description   = "Alert on unauthorized API calls"
  metric_name         = "UnauthorizedAPICallsMetric"
  namespace           = "CloudTrailMetrics"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions       = [aws_sns_topic.security_alerts.arn]
  treat_missing_data  = "notBreaching"
}

# Metric Filter - Root Account Usage
resource "aws_cloudwatch_log_group_metric_filter" "root_account_usage" {
  name           = "RootAccountUsageMetricFilter"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name
  filter_pattern = "{ $.userIdentity.type = \"Root\" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != \"AwsServiceEvent\" }"

  metric_transformation {
    name      = "RootAccountUsageMetric"
    namespace = "CloudTrailMetrics"
    value     = "1"
  }
}

# Alarm - Root Account Usage
resource "aws_cloudwatch_metric_alarm" "root_account_usage" {
  alarm_name          = "SecurityAlert-RootAccountUsage"
  alarm_description   = "Alert on root account usage"
  metric_name         = "RootAccountUsageMetric"
  namespace           = "CloudTrailMetrics"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions       = [aws_sns_topic.security_alerts.arn]
  treat_missing_data  = "notBreaching"
}

# Metric Filter - IAM Policy Changes
resource "aws_cloudwatch_log_group_metric_filter" "iam_policy_changes" {
  name           = "IAMPolicyChangesMetricFilter"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name
  filter_pattern = "{ ($.eventName = DeleteGroupPolicy) || ($.eventName = DeleteRolePolicy) || ($.eventName = DeleteUserPolicy) || ($.eventName = PutGroupPolicy) || ($.eventName = PutRolePolicy) || ($.eventName = PutUserPolicy) || ($.eventName = CreatePolicy) || ($.eventName = DeletePolicy) || ($.eventName = CreatePolicyVersion) || ($.eventName = DeletePolicyVersion) || ($.eventName = AttachRolePolicy) || ($.eventName = DetachRolePolicy) || ($.eventName = AttachUserPolicy) || ($.eventName = DetachUserPolicy) || ($.eventName = AttachGroupPolicy) || ($.eventName = DetachGroupPolicy) }"

  metric_transformation {
    name      = "IAMPolicyChangesMetric"
    namespace = "CloudTrailMetrics"
    value     = "1"
  }
}

# Alarm - IAM Policy Changes
resource "aws_cloudwatch_metric_alarm" "iam_policy_changes" {
  alarm_name          = "SecurityAlert-IAMPolicyChanges"
  alarm_description   = "Alert on IAM policy changes"
  metric_name         = "IAMPolicyChangesMetric"
  namespace           = "CloudTrailMetrics"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions       = [aws_sns_topic.security_alerts.arn]
  treat_missing_data  = "notBreaching"
}

# Metric Filter - MFA Disable
resource "aws_cloudwatch_log_group_metric_filter" "mfa_disable" {
  name           = "MFADisableMetricFilter"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name
  filter_pattern = "{ ($.eventName = DeactivateMFADevice) || ($.eventName = DeleteVirtualMFADevice) }"

  metric_transformation {
    name      = "MFADisableMetric"
    namespace = "CloudTrailMetrics"
    value     = "1"
  }
}

# Alarm - MFA Disable
resource "aws_cloudwatch_metric_alarm" "mfa_disable" {
  alarm_name          = "SecurityAlert-MFADisable"
  alarm_description   = "Alert on MFA device deactivation"
  metric_name         = "MFADisableMetric"
  namespace           = "CloudTrailMetrics"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  alarm_actions       = [aws_sns_topic.security_alerts.arn]
  treat_missing_data  = "notBreaching"
}

# Outputs
output "cloudtrail_arn" {
  description = "CloudTrail ARN"
  value       = aws_cloudtrail.main.arn
}

output "cloudtrail_s3_bucket" {
  description = "S3 bucket for CloudTrail logs"
  value       = aws_s3_bucket.cloudtrail_logs.id
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group"
  value       = aws_cloudwatch_log_group.cloudtrail_logs.name
}

output "sns_topic_arn" {
  description = "SNS topic for security alerts"
  value       = aws_sns_topic.security_alerts.arn
}
