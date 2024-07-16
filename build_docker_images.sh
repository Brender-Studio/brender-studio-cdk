#!/bin/bash

REPO_ECR_NAME=$1
BLENDER_VERSIONS=$2
AWS_ACCOUNT_ID=$3
AWS_DEFAULT_REGION=$4

echo "Building docker images for Blender versions: $BLENDER_VERSIONS"
echo "AWS ECR Repository: $REPO_ECR_NAME"
echo "AWS Account ID: $AWS_ACCOUNT_ID"
echo "AWS Default Region: $AWS_DEFAULT_REGION"

get_major_version() {
    major_version=$1
    echo "$major_version"
}

get_full_version() {
    version=$1
    full_version="${version%.*}"  # Extract major version from full version
    echo "$full_version"
}

image_exists_in_ecr() {
    major_version=$1
    image_exists=$(docker manifest inspect $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$major_version 2>&1)
    
    if [[ $image_exists == *"no such manifest"* ]]; then
        return 1
    else
        return 0
    fi
}

build_and_push_image() {
    full_version=$1
    major_version=$2

    # Check if image exists in ECR
    image_exists_in_ecr $major_version
    if [ $? -eq 0 ]; then
        echo "Image already exists in ECR for major version: $major_version"
    else
        echo "Image does NOT exist in ECR for major version: $major_version" 
        # Build docker image
        cd docker_blender
        docker build -t $REPO_ECR_NAME:$major_version --build-arg BLENDER_VERSION=$full_version --build-arg BLENDER_VERSION_MAJOR=$major_version .
        docker tag $REPO_ECR_NAME:$major_version $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$major_version
        docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$major_version
        cd ..
        echo "Docker image for Blender version: $full_version with major version: $major_version has been built and pushed to ECR"

    fi

}

IFS=',' read -ra VERSION_ARRAY <<< "$BLENDER_VERSIONS"

for VERSION in "${VERSION_ARRAY[@]}"; do 
    major_version=$(get_major_version $VERSION)
    full_version=$(get_full_version $VERSION)
    echo "Building docker image for Blender version: $full_version with major version: $major_version"
    build_and_push_image $full_version $major_version

done