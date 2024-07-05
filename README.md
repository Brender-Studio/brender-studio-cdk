# Brender Studio CDK

## Description

This repository contains the AWS infrastructure (CDK), Docker image, and logic related to rendering jobs for Brender Studio. It also includes a shell script for compiling and pushing Docker images.

## Repository Structure

- `aws_cdk/`: Defines the infrastructure for the farms created with Brender Studio.
- `docker_blender/`: Contains the Dockerfile and all necessary logic, written in Python. This Docker image is used to run Blender jobs.
- `build_docker_images.sh`: Script that receives an array of Blender versions as parameters, builds them, and pushes them to ECR (blender-repo-ecr).

## Key Components

1. **AWS CDK Stack**: Defined in `aws_cdk/`, this creates the necessary AWS resources including VPC, Security Groups, EFS, S3 Bucket, and AWS Batch resources.

2. **Docker Image**: The Dockerfile in `docker_blender/` sets up an environment with Blender and required dependencies.

3. **Build Script**: `build_docker_images.sh` automates the process of building and pushing Docker images for different Blender versions.

## Usage

This infrastructure is deployed using AWS CodeBuild, which automates the creation of resources needed for Brender Studio farms.

### Deployment Process

The deployment process is initiated from the Brender Studio application. Here's how it works:

1. Using the Brender Studio app ([brender-studio-app repository](https://github.com/Brender-Studio/brender-studio-app)), a CodeCommit repository is created.
2. A buildspec.yml file is uploaded to this CodeCommit repository.
3. This triggers a CodeBuild task that executes the infrastructure deployment.

The buildspec.yml file used for CodeBuild can be found here: [buildspec.yml](https://github.com/Brender-Studio/brender-studio-app/blob/main/src-tauri/resources/deploy/buildspec.yml)

This buildspec.yml handles:
- Setting up the build environment
- Cloning this repository (brender-studio-cdk)
- Building and pushing Docker images
- Deploying the CDK stack

### Example Deployment Command

While the actual deployment is handled by CodeBuild, here's an example of the kind of command it might use:

```bash
cdk deploy --context stackName=BRENDER-STACK-DEMO \
           --parameters ecrRepoName=blender-repo-ecr \
           --context blenderVersions="3.6.0,4.1.1" \
           --context isPrivate="true" \
           --context maxvCpus='{"onDemandCPU": "100", "spotCPU": "256", "onDemandGPU": "100", "spotGPU": "256"}' \
           --context spotBidPercentage='{"spotCPU": "80", "spotGPU": "90"}' \
           --context useG6Instances="true" \
           --region us-east-1
```

## References

This project makes use of several AWS services and other technologies:

- [AWS CDK (Cloud Development Kit)](https://aws.amazon.com/cdk/): Used for defining cloud infrastructure in code and provisioning it through AWS CloudFormation.
- [AWS CloudFormation](https://aws.amazon.com/cloudformation/): Manages and provisions all the cloud infrastructure resources in the AWS environment.
- [AWS CodeBuild](https://aws.amazon.com/codebuild/): Fully managed continuous integration service that compiles source code, runs tests, and produces software packages.
- [Docker](https://www.docker.com/): Platform used to build, manage, and deploy containerized applications.
- [Amazon ECR (Elastic Container Registry)](https://aws.amazon.com/ecr/): Fully managed Docker container registry that makes it easy to store, manage, and deploy Docker container images.
- [AWS Batch](https://aws.amazon.com/batch/): Used for running batch computing workloads on AWS.
- [Amazon EFS (Elastic File System)](https://aws.amazon.com/efs/): Provides scalable file storage for use with AWS cloud services and on-premises resources.
- [Amazon S3 (Simple Storage Service)](https://aws.amazon.com/s3/): Object storage service used for storing and retrieving data.


For more information on how these services are used in the context of Brender Studio, please refer to the code and comments within this repository.
