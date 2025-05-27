aws_region            = "us-east-1"
environment           = "dev"
image_tag             = "dev"
ghcr_user             = "rainer85ah"

vpc_name              = "mcp-dev-vpc"
vpc_cidr              = "10.0.0.0/16"
public_subnet_cidrs   = ["10.0.1.0/24"]
private_subnet_cidrs  = ["10.0.2.0/24"]

# Replace the IAM role ARNs with actual ones from your AWS account.
ecs_execution_role_arn = "arn:aws:iam::1234567890:role/ecsTaskExecutionRole-dev"
