aws_region     = "us-east-1"
environment    = "development"
vpc_cidr       = "10.0.0.0/16"
public_subnet_cidr  = "10.0.1.0/24"
private_subnet_cidr = "10.0.2.0/24"
instance_type  = "t2.micro"
enable_monitoring = true

tags = {
  Project     = "cloud-security-automation"
  Team        = "DevOps"
  CostCenter  = "Engineering"
  ManagedBy   = "Terraform"
}
