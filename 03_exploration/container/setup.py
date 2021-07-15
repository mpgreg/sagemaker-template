REGION='eu-west-1'
ACCOUNT_ID=''
REPO_NAME='smstudio-custom'
IMAGE_NAME='custom-r'
ROLE_ARN=''


aws --region ${REGION} ecr get-login-password | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}

aws ecr describe-repositories --region ${REGION} --repository-names "${REPO_NAME}" > /dev/null 2>&1

if [ $? -ne 0 ]
then 
    aws ecr create-repository --region ${REGION} --repository-name "${REPO_NAME}" > /dev/null
fi

docker build . -t ${IMAGE_NAME} -t ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/smstudio-custom:${IMAGE_NAME}

docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_NAME}

aws --region ${REGION} sagemaker create-image \
    --image-name ${IMAGE_NAME} \
    --role-arn ${ROLE_ARN}

aws --region ${REGION} sagemaker create-image-version \
    --image-name ${IMAGE_NAME} \
    --base-image "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_NAME}"

# Verify the image-version is created successfully. Do NOT proceed if image-version is in CREATE_FAILED state or in any other state apart from CREATED.
aws --region ${REGION} sagemaker describe-image-version --image-name ${IMAGE_NAME}

aws --region ${REGION} sagemaker create-app-image-config --cli-input-json file://app-image-config-input.json

aws --region ${REGION} sagemaker update-domain --cli-input-json file://update-domain-input.json

import boto3
