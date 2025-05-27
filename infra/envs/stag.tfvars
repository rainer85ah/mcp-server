aws_region            = "us-east-1"
environment           = "stag"
ghcr_user             = "rainer85ah"
image_tag             = "stag"

vpc_name              = "mcp-stag-vpc"
vpc_cidr              = "10.30.0.0/16"
public_subnet_cidrs   = ["10.30.1.0/24", "10.30.2.0/24"]
private_subnet_cidrs  = ["10.30.3.0/24", "10.30.4.0/24"]

# Replace the IAM role ARNs with actual ones from your AWS account.
ecs_execution_role_arn = "arn:aws:iam::123456789012:role/ecsTaskExecutionRole-stag"
