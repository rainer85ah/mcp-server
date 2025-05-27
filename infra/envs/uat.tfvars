aws_region            = "us-east-1"
environment           = "uat"
ghcr_user             = "rainer85ah"
image_tag             = "uat"

vpc_name              = "mcp-uat-vpc"
vpc_cidr              = "10.20.0.0/16"
public_subnet_cidrs   = ["10.20.1.0/24", "10.20.2.0/24"]
private_subnet_cidrs  = ["10.20.3.0/24", "10.20.4.0/24"]

# Replace the IAM role ARNs with actual ones from your AWS account.
ecs_execution_role_arn = "arn:aws:iam::123456789012:role/ecsTaskExecutionRole-uat"
