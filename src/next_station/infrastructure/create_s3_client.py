import boto3
from mypy_boto3_s3 import S3Client
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, NoRegionError, EndpointConnectionError
from .exceptions import S3ConfigError, S3ConnectionError

def create_s3_client() -> S3Client:

    try:
        
        return boto3.client('s3')
    
    except (NoCredentialsError, PartialCredentialsError) as nce:
        raise S3ConfigError(f"AWS S3 - No credentials found. Check your AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY") from nce


    except NoRegionError as nre:
        raise S3ConfigError(f"AWS S3 - Region for client S3 not specified!") from nre


    except EndpointConnectionError as ece:
        raise S3ConnectionError(f"AWS S3 - Could not connect to the endpoint. Please check your internet or AWS service status") from ece
