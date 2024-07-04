import os
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import boto3.session

bucket_name = os.environ.get('BUCKET_NAME')
bucket_key = os.environ.get('BUCKET_KEY')

# review args if needed!!!

def generate_presigned_urls(region):
    try:
        session = boto3.session.Session(region_name=region)
        
        s3_client = session.client('s3', config=Config(signature_version='s3v4'))

        # Generate presigned url for thumbnail
        thumbnail_presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{bucket_key}/bs_thumbnail.png"
            },
            ExpiresIn=604800  # 1 week
        )
        # Generate presigned url for output.zip
        output_zip_presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{bucket_key}/output.zip"
            },
            ExpiresIn=604800  # 1 week
        )
        return thumbnail_presigned_url, output_zip_presigned_url
    except ClientError as e:
        print(f"Error: {e.response['Error']['Code']}")
        return None, None 