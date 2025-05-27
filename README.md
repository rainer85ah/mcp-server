[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


# 🚀 Terraform - Manage AWS ECS

This repository contains the Terraform configuration to provision and manage the AWS infrastructure for the **MCP Service**. The infrastructure is designed to support multiple environments (development, staging, UAT, and production) using AWS ECS (Elastic Container Service) with Fargate, along with networking and security components.

---

## 🧱 Features

- Modular design separating **networking** and **ECS service** components.
- Multi-environment support: `dev`, `uat`, `stag`, and `prod`.
- VPC with public and private subnets, security groups, and ALB (Application Load Balancer).
- ECS Cluster and Fargate service deployment with task definitions.
- Dynamic image tagging to match environment branches or commit SHAs for traceability.
- Secure handling of IAM roles and permissions.

---

## Prerequisites

- Terraform v1.5.0 or later
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create VPCs, ECS clusters, ALBs, IAM roles, etc.
- Docker images built and pushed to GHCR (GitHub Container Registry)
- Variables files (`terraform.tfvars`) per environment with appropriate values

## 📦 Getting Started with workspace:

```bash

terraform init
terraform workspace new prod
terraform plan -var-file="prod.tfvars"
terraform apply -var-file="envs/prod.tfvars"
```

## 🚀 How to Deploy Per Env

```bash

terraform init
terraform plan -var-file="environments/dev.tfvars"
terraform apply -var-file="environments/dev.tfvars"
```


## 📜 License


This project is licensed under the [MIT License](https://opensource.org/license/mit).  
You are free to use, modify, and distribute this software with proper attribution.


## 📫 Contact

Created with 💡 by **Rainer Arencibia**  
🔗 Connect with me on [LinkedIn](https://www.linkedin.com/in/rainer-arencibia)
