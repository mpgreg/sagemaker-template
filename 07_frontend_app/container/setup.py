#https://docs.aws.amazon.com/sagemaker/latest/dg/processing-container-run-scripts.html


import boto3
account_id = boto3.client('sts').get_caller_identity().get('Account')
region = boto3.session.Session().region_name

ecr_repository = 'sagemaker-spark-example'
tag = ':latest'
uri_suffix = 'amazonaws.com'
if region in ['cn-north-1', 'cn-northwest-1']:
    uri_suffix = 'amazonaws.com.cn'
spark_repository_uri = '{}.dkr.ecr.{}.{}/{}'.format(account_id, region, uri_suffix, ecr_repository + tag)

# Create ECR repository and push docker image
!$(aws ecr get-login --region $region --registry-ids $account_id --no-include-email)
!aws ecr create-repository --repository-name $ecr_repository
!docker tag {ecr_repository + tag} $spark_repository_uri
!docker push $spark_repository_uri