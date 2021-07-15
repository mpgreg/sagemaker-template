#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url
#https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-post-example.html

#aws --profile ds1p1 s3api put-object --bucket lz --key upload/
#aws --profile adminp1 s3 presign s3://lz/upload/Tweets.csv --expires-in 604800

#generate_presigned_url(ClientMethod, Params=None, ExpiresIn=3600, HttpMethod=None)¶
#generate_presigned_post(Bucket, Key, Fields=None, Conditions=None, ExpiresIn=3600)¶



import boto3
import requests
region = boto3.Session(profile_name='default').region_name
s3 = boto3.client('s3', region_name=region)

headers={'Content-Type':type}

url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': 'lz', 'Key': 'upload/test.txt', 'ContentType': 'application/octet-stream' },
        ExpiresIn=3600,
    )

url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': 'lz', 'Key': 'upload/test.txt'},
        ExpiresIn=3600,
    )

s3.generate_presigned_post('lz', 'upload/test.txt', ExpiresIn=3600)


files = StringIO("asdfasdfasdf")
response = requests.put(url, data=files)

print(str(response.content))


def s3_upload_creds(name):
    BUCKET = ''
    REGION = 'eu-west-1'
    s3 = boto3.client('s3', region_name=REGION, config=Config(signature_version='s3v4'))
    key = '${filename}'
    return s3.generate_presigned_post(Bucket = BUCKET, Key = key)

s3_upload_creds('test.txt')



# Make sure everything posted is publicly readable
fields = {"acl": "public-read"}

# Ensure that the ACL isn't changed and restrict the user to a length
# between 10 and 100.
conditions = [
    {"acl": "public-read"},
    ["content-length-range", 1, 1048576] # i changed this from 10-100 to 1-1048576 i'm quite sure these are bytes.
]

# Generate the POST attributes
post = s3.generate_presigned_post(
    Bucket='',
    Key='upload/test.txt',
    Fields=fields,
    Conditions=conditions
)
