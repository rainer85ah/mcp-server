variable "environment" {}
variable "vpc_id" {}
variable "public_subnet_ids" {
  type = list(string)
}
variable "image_tag" {}
variable "ecs_execution_role_arn" {}
variable "ghcr_user" {}
