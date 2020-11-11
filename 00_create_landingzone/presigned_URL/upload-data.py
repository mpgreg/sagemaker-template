#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url
#https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-post-example.html

#http://project1-lz.s3-website-eu-west-1.amazonaws.com

#aws --profile ds1p1 s3api put-object --bucket project1-lz --key upload/
#aws --profile adminp1 s3 presign s3://project1-lz/upload/Tweets.csv --expires-in 604800

#https://project1-lz.s3.eu-west-1.amazonaws.com/upload/?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQAFUNCGWAMXFLREQ%2F20201006%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Date=20201006T173911Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCWV1LXdlc3QtMSJHMEUCIBZth3f%2F6kCrMlpAB%2BYzZHK2L9QFMtyipNBx1mVSBF0bAiEA4nvGTE1i8EHwZBPvIxMmySuqzhBYiqpWCizeUQsXBl0qwAII8%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwwMDAzNzgzNDM4NTIiDI1mehj88nA13FRsrSqUAhay2Z8IqRdC197%2FIuHi5VaRn2Oekjb40smBIKqKnsrfoRoQVH%2BrCUhUadlSx9u3hfWWYFZiZOv7Fq8cTpZcD%2BUvt%2F8JviPYJxonX%2BsRjUBhcjc9TGfcQAFvbCe8byFaiIluCzvMhXXcYT3%2BCm0TtT5gRvCRy%2BsvSAUZI1XmPzM03nW5tBFEf2n3SndQrPKYjpymPSs5bcTZuH1P1Q1VpNrF7ok5pVupvFyhQMOyQFuA8tcfEUszkQOlE%2B4c0UKnr%2BFB4VUacx70GaSasOjMNeBg3Foj4BKJd62a3A8DfruMP92mxumc7lRmn92sBpQF7bSe9J7KX8D0tzn430uQqDtKIZbSA65tPS2RfeWfPDw%2F9gB1TzCx0%2FL7BTqkAcDkfLj%2FO%2F6nFRXebNqIsB2FfNgAzI6OuyvlNL3hDQuzYWp4zMG2HnKxW8%2Fwdb%2B9nY9PE%2F3jzTW57A3Rv9GaYgDZxeIcB2t3iILu3VEKYmXNoAni9uByaEZtDsyFcyVfW2QM4845WmuYXMHGgOAFCi6%2BXZFfCQfDlqaa8Ps4b8ELBcv%2Bs0R5kReHYfHjzIpzE35iL1dlfPeGd1Bv8%2F%2BRR179EOmF&X-Amz-Signature=b7e74c71cdb11280af81c48d162bc9fabc98641d55ac8a82981abdda2a9e428d


#generate_presigned_url(ClientMethod, Params=None, ExpiresIn=3600, HttpMethod=None)¶
#generate_presigned_post(Bucket, Key, Fields=None, Conditions=None, ExpiresIn=3600)¶



import boto3
import requests
region = boto3.Session(profile_name='default').region_name
s3 = boto3.client('s3', region_name=region)

headers={'Content-Type':type}

url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': 'project1-lz', 'Key': 'upload/test.txt', 'ContentType': 'application/octet-stream' },
        ExpiresIn=3600,
    )

url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': 'project1-lz', 'Key': 'upload/test.txt'},
        ExpiresIn=3600,
    )

s3.generate_presigned_post('project1-lz', 'upload/test.txt', ExpiresIn=3600)


files = StringIO("asdfasdfasdf")
response = requests.put(url, data=files)

print(str(response.content))


def s3_upload_creds(name):
    BUCKET = 'project1-lz'
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
    Bucket='project1-lz',
    Key='upload/test.txt',
    Fields=fields,
    Conditions=conditions
)
