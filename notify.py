import boto3
from botocore.exceptions import NoCredentialsError
from twilio.rest import Client


ACCESS_KEY = ''
SECRET_KEY = ''
bucket = ""
def upload_to_aws(local_file,s3_file):
    msg = 'ALERT, there is something wrong. '
    print(local_file)
    print(s3_file)
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'GrantFullControl': 'uri="#"',"ContentType": "application/octet-stream", "ContentEncoding": "video/mp4"})
    print("Upload Successful")
    url = "#" + s3_file
    client = Client("#","#")
    msg = msg + url
    client.messages.create(to="#", from_="#", body=msg)
    
    # delete the temporary file
    return True


