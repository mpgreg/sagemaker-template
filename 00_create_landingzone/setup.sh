Create the Serverless application (https://console.aws.amazon.com/lambda/home?region=us-east-1#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:520945424137:applications/cloudfront-authorization-at-edge) for Authentication at the Edge
    -Optionally customize/build from the yaml template (attached)
	    -For some reason this one only works in us-east-1 but should be able to fix that.
    -Optionally include email address for first cognito user
    -Replace the HttpHeaders with {}

After creation note the following:
    -the cloudfront domain name (ie. dwoxt2hwst627.cloudfront.net)
    -the S3 bucket (ie. serverlessrepo-cloudfront-authorization-s3bucket-1r8gz363fpgdj)

Upload the S3 explorer JS app to the cloud front bucket
	#git clone -b v2-alpha https://github.com/awslabs/aws-js-s3-explorer
	#aws s3 sync . s3://serverlessrepo-cloudfront-authorization-s3bucket-1r8gz363fpgdj --exclude ".*"

Create another S3 bucket for the upload location (landing zone) and setup CORS with domain name from cloudfront as allowed origins
    -see attached json
    -update the AllowedOrigins
        "AllowedOrigins": [
            "https://dwoxt2hwst627.cloudfront.net",
            "https://dwoxt2hwst627.cloudfront.net/"],

Go to the cloud front deployment and modify 
	Default behavior 
		"Allowed HTTP Methods" to "GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE” 
		"Cache and origin request” to "Use a cache policy and origin request policy”
		"Cache Policy" to "Managed-Caching-Optimized” 
		"Origin Request Policy" to "Managed-CORS-S3-Origin”:

Create a token for the user:
	#aws sts get-session-token --region us-east-1 --duration-seconds 7200

User gets an email with password.  Login at dwoxt2hwst627.cloudfront.net and configure with token provided above

