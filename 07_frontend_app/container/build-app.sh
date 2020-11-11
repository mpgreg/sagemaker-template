#!/bin/sh

mkdir container
cd container
cp ../../app/dashboard.py .
cp ../../data/umap_embedding.joblib .
cp ../Dockerfile .

# The name of our algorithm
algorithm_name='airline-sentiment'
cli_profile='ds1p1'
pull_account=`grep ^FROM Dockerfile | cut -d" " -f2 | cut -d. -f1`
pull_region=`grep ^FROM Dockerfile | cut -d" " -f2 | cut -d. -f4`
push_account=`aws --profile ${cli_profile} sts get-caller-identity --query Account --output text`
push_region=`aws configure get region`
fullname="${push_account}.dkr.ecr.${push_region}.amazonaws.com/${algorithm_name}:latest"

# Get the login command from ECR and execute it directly
aws --profile ${cli_profile} ecr get-login-password --region ${push_region} | docker login --username AWS --password-stdin ${push_account}.dkr.ecr.${push_region}.amazonaws.com

# If the repository doesn't exist in ECR, create it.

aws --profile ${cli_profile} ecr describe-repositories --region ${push_region} --repository-names "${algorithm_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws --profile ${cli_profile} ecr create-repository --region ${push_region} --repository-name "${algorithm_name}" > /dev/null
fi


# Get the login command from ECR in order to pull down the SageMaker PyTorch image
aws --profile ${cli_profile} ecr get-login-password --region ${pull_region} | docker login --username AWS --password-stdin ${pull_account}.dkr.ecr.${pull_region}.amazonaws.com

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build  -t ${algorithm_name} . --build-arg REGION=${push_region}
docker tag ${algorithm_name} ${fullname}

docker push ${fullname}

