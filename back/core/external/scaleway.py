import logging

import boto3
import requests
from botocore.exceptions import ClientError

from core.config import SETTINGS


def upload_file(binary_file, name = None):

    object_name = binary_file.name if name is None else name

    session = boto3.session.Session()

    s3_client = session.client(
        service_name='s3',
        region_name=SETTINGS.SCALEWAY_S3_REGION,
        use_ssl=True,
        endpoint_url=SETTINGS.SCALEWAY_S3_URL,
        aws_access_key_id=SETTINGS.SCALEWAY_S3_KEY_ID,
        aws_secret_access_key=SETTINGS.SCALEWAY_S3_ACCESS_KEY
    )

    bucket_name = "scan"
    fields = {
        "acl": "public-read",
        "Cache-Control": "nocache",
        "Content-Type": "image/jpeg"
    }
    conditions = [
        {"key": object_name},
        {"acl": "public-read"},
        {"Cache-Control": "nocache"},
        {"Content-Type": "image/jpeg"}
    ]
    expiration = 120  # Max two minutes to start upload

    try:
        response = s3_client.generate_presigned_post(Bucket=bucket_name,
                                                     Key=object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
    files = {'file': (object_name, binary_file)}
    http_response = requests.post(response['url'], data=response['fields'], files=files)
    print(http_response.content)


with open('0.jpg', 'rb') as f:
    upload_file(f)
