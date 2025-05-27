provider "aws" {
  region = var.aws_region
}

module "networking" {
  source               = "./modules/networking"
  vpc_name             = var.vpc_name
  cidr_block           = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  environment          = var.environment
}

module "ecs_service" {
  source               = "./modules/ecs-service"

  cluster_name         = "mcp-${var.environment}-cluster"
  service_name         = "mcp-${var.environment}-service"
  container_name       = "mcp"
  container_port       = 8000
  image                = "ghcr.io/${var.ghcr_user}/mcp-service:${var.image_tag}"

  vpc_id               = module.networking.vpc_id
  subnet_ids           = module.networking.private_subnet_ids
  security_group_ids   = [module.networking.service_sg_id]

  assign_public_ip     = true
  cpu                  = 512
  memory               = 1024
  execution_role_arn   = var.ecs_execution_role_arn
  desired_count        = 1
  target_group_arn     = module.networking.target_group_arn

  environment          = var.environment
}
