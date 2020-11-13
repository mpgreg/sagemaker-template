# In[ ]:

import boto3
from sagemaker import get_execution_role
import time

#role = get_execution_role()
role = 'arn:aws:iam::000378343852:role/service-role/AmazonSageMaker-ExecutionRole-20200929T192105'

project_name = 'project1'

endpoint_name = project_name+'_python_REPL_'+time.strftime("%Y%m%d-%H%M%S")
private_key_file="~/.ssh/"+endpoint_name+"_private.key"
public_key_file="~/.ssh/"+endpoint_name+"_public.key"

# In[ ]:
#create ssh key
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from os import chmod

key = rsa.generate_private_key(
    backend=crypto_default_backend(),
    public_exponent=65537,
    key_size=2048
)

private_key = key.private_bytes(
    crypto_serialization.Encoding.PEM,
    crypto_serialization.PrivateFormat.OpenSSH,
    crypto_serialization.NoEncryption())

public_key = key.public_key().public_bytes(
    crypto_serialization.Encoding.OpenSSH,
    crypto_serialization.PublicFormat.OpenSSH
)

#save files for ssh tunnel setup
with open(private_key_file, 'wb') as f:
    chmod(private_key_file, 0o600)
    f.write(private_key)
    f.close

with open(public_key_file, 'wb') as f:
    f.write(public_key)
    f.close      

# In[ ]:
#create lib zip

# In[ ]:
public_key_string=public_key.decode()+" junk@junk.com"

gl_client = boto3.client('glue')
response = gl_client.create_dev_endpoint(
    EndpointName=endpoint_name,
    RoleArn=role,
    #SecurityGroupIds=[
    #    '',
    #],
    #SubnetId='',
    PublicKey=public_key_string,
    NumberOfNodes=2,
    #WorkerType='Standard',
    GlueVersion='1.0',   #GV 1.0 for python 3.6, GV2.0 for python 3.7
    #NumberOfWorkers=1,
    #ExtraPythonLibsS3Path='string',
    #ExtraJarsS3Path='string',
    #SecurityConfiguration='string',
    #Tags={
    #    'string': 'string'
    #},
    Arguments={
        'GLUE_PYTHON_VERSION' : '3'
    }
)

gl_client.get_dev_endpoint(EndpointName=response['EndpointName'])['DevEndpoint']

import time

# Wait until change set status is CREATE_COMPLETE
while True:
    endpoint_status = gl_client.get_dev_endpoint(EndpointName=response['EndpointName'])['DevEndpoint']['Status']
    print(str(endpoint_status))
    if endpoint_status == 'READY':
        break
    time.sleep(10)


# In[ ]:


endpoint_ipaddress = gl_client.get_dev_endpoint(EndpointName=response['EndpointName'])['DevEndpoint']['PublicAddress']

print("Python3 Endpoint: \n"
"ssh -i " + private_key_file + " glue@" + endpoint_ipaddress + " -t python3"+"\n")

print("SSH Tunnel Endpoint: \n"
"ssh -i " + private_key_file + " -vnNT -L :9007:169.254.76.1:9007 glue@" + endpoint_ipaddress + "\n")

print("PySpark Endpoint: \n"
"ssh -i " + private_key_file + " glue@" + endpoint_ipaddress + " -t gluepyspark"+"\n")

print("Scala Endpoint: \n"
"ssh -i " + private_key_file + " glue@" + endpoint_ipaddress + " -t glue-spark-shell")


# In[ ]:


#####NOTE: Don't forget to delete the endpoint when no longer in-use.#####
import os
gl_client.delete_dev_endpoint(EndpointName=response['EndpointName'])


if os.path.exists(public_key_file):
    os.remove(public_key_file)

if os.path.exists(private_key_file):
    os.remove(private_key_file)

