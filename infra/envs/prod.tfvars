aws_region            = "us-east-1"
environment           = "prod"
ghcr_user             = "rainer85ah"
image_tag             = "latest"

vpc_name              = "mcp-prod-vpc"
vpc_cidr              = "10.40.0.0/16"
public_subnet_cidrs   = ["10.40.1.0/24", "10.40.2.0/24"]
private_subnet_cidrs  = ["10.40.3.0/24", "10.40.4.0/24"]

# Replace the IAM role ARNs with actual ones from your AWS account.
ecs_execution_role_arn = "arn:aws:iam::123456789012:role/ecsTaskExecutionRole-prod"
