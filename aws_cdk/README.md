# Brender Studio CDK Infrastructure

This project contains the AWS CDK infrastructure code for Brender Studio, a system designed to deploy render farms for Blender using AWS Batch.

## Overview

Brender Studio uses AWS CDK to define and deploy its infrastructure. The main components include:

- VPC configuration
- Security Groups
- AWS Batch resources (Compute Environments, Job Queues, and Job Definitions)
- Amazon EFS for shared storage
- S3 bucket for asset storage

For testing purposes, the infrastructure also includes:
- Lambda function for listing EFS contents
- API Gateway for accessing the Lambda function

The infrastructure is designed to support both CPU and GPU-based rendering, with options for on-demand and spot instances.

## Key Components

### VPC and Security

- Creates a VPC with public or private subnets based on configuration
- Sets up necessary security groups

### Storage

- Configures Amazon EFS for shared file storage
- Creates an S3 bucket for asset storage

### AWS Batch

- Sets up Compute Environments for both CPU and GPU instances
- Creates Job Queues for different instance types
- Defines Job Definitions for various Blender versions

### Lambda and API Gateway (Testing)

- Deploys a Lambda function for listing EFS contents
- Sets up an API Gateway to access the Lambda function

## Deployment

The infrastructure is deployed using AWS CodeBuild. The deployment process takes several parameters to customize the stack:

- ECR repository name
- Blender versions
- Private/Public VPC configuration
- Max vCPUs for different instance types
- Spot bid percentage
- Option to use G6 instances

## Docker Images

While not directly part of this CDK code, the real power of Brender Studio lies in the Docker images used in the Job Definitions. These images are pre-configured with Blender and optimized for rendering in an AWS Batch environment.

The `docker_blender` directory contains the Dockerfile and logic for building these images. The `build_docker_images.sh` script automates the process of building and pushing Docker images for different Blender versions.

## Usage

To deploy the stack, use the following command format:

> [!WARNING] 
> You must create an ECR repository before running the deployment command. Docker images must be pushed to this repository before deploying the stack.

```bash
cdk deploy --context stackName=BRENDER-STACK-DEMO \
           --parameters ecrRepoName=blender-repo-ecr \
           --context blenderVersions="3.6.0,4.1.1" \
           --context isPrivate="true" \
           --context maxvCpus='{"onDemandCPU": "100", "spotCPU": "256", "onDemandGPU": "100", "spotGPU": "256"}' \
           --context spotBidPercentage='{"spotCPU": "80", "spotGPU": "90"}' \
           --context useG6Instances="true" \
           --context account=${AWS_ACCOUNT_ID} \
           --region us-east-1
```

