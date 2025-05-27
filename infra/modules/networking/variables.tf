variable "environment" {}
variable "vpc_cidr" {}
variable "public_subnet_cidrs" {
  type = list(string)
}
