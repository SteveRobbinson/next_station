import requests
import logging
import json
import boto3
from mypy_boto3_s3 import S3Client
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    NoRegionError,
    EndpointConnectionError,
    ClientError
)

from src.next_station.core.exceptions import (
    S3ServiceError,
    S3ConfigError,
    S3ConnectionError,
    S3AccessDeniedError,
    S3NotFoundError
)

from .runner import runner
from src.next_station.schemas.worldpop import ApiMetadata, S3Etag
from pydantic import ValidationError
from typing import List
import io


def create_s3_client() -> S3Client:

    try:
        
        return boto3.client('s3')
    
    except (NoCredentialsError, PartialCredentialsError) as nce:
        raise S3ConfigError(f"AWS S3 - No credentials found. Check your AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY") from nce


    except NoRegionError as nre:
        raise S3ConfigError(f"AWS S3 - Region for client S3 not specified!") from nre


    except EndpointConnectionError as ece:
        raise S3ConnectionError(f"AWS S3 - Could not connect to the endpoint. Please check your internet or AWS service status") from ece


logger = logging.getLogger(__name__)

def get_s3_object_metadata(s3client: S3Client,
                           bucket_name: str,
                           file_name_on_s3: str
                           ) -> dict:

    try:
        
        aws_response = s3client.get_object(
            Bucket = bucket_name,
            Key = file_name_on_s3)

        metadata = json.load(aws_response['Body'])

        return metadata

    
    except ClientError as ce:
        

        status_code = ce.response['Error']['Code']
        
        if status_code == '403':
            raise S3AccessDeniedError(f"AWS S3 - Access denied. Status code: {status_code}\nProvided credentials do not have permissions to access S3 resources") from ce

        elif status_code in('404', 'NoSuchKey'):
            logger.info("Metadata not found for %s. Starting fresh.", file_name_on_s3)
            return {}

        else:
            raise S3ServiceError(f"AWS S3 - Client Error occurred! Status code: {status_code}") from ce



def compare_metadata(s3_metadata: dict,
                     file_url: str
                    ) -> bool:
    
    if not s3_metadata:
        return False

    try:

        api_response = runner(file_url, 'head')
        api_etag = ApiMetadata(**api_response.headers).etag

        aws_s3_etag = S3Etag(**s3_metadata).s3_etag

        return aws_s3_etag == api_etag
    
    except ValidationError:
        return False



def upload_data_to_s3(bucket_name: str,
                      file_name: str,
                      object_to_upload: requests.Response,
                      s3_client: S3Client,
                      metadata: dict | None = None
                      ) -> bool:

    extra_args = {'Metadata': metadata} if metadata else {}

    s3_client.upload_fileobj(Bucket = bucket_name,
                             Fileobj = object_to_upload.raw,
                             Key = file_name,
                             ExtraArgs = extra_args)

    return True
