import requests
import json
import boto3
from mypy_boto3_s3 import S3Client
from src.next_station.core.exceptions import S3ServiceError
from .runner import runner
from src.next_station.schemas.worldpop import ApiMetadata, S3Etag
from typing import List, Any
import io


def create_s3_client() -> S3Client:

    try:
        
        return boto3.client('s3')
    
    except Exception as err:
        raise S3ServiceError.from_exception(err) from err


def get_s3_object_metadata(s3client: S3Client,
                           aws_s3_path: str,
                           metadata_file_name: str = 'metadata.json'
                           ) -> dict:

    try:
        
        aws_response = s3client.get_object(
            Bucket = aws_s3_path,
            Key = metadata_file_name)

        metadata = json.load(aws_response['Body'])

        return metadata
    
    except Exception as err:
        raise S3ServiceError.from_exception(err) from err


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
    
    except Exception as err:
        raise S3ServiceError.from_exception(err) from err


def upload_data_to_s3(bucket_name: str,
                      file_name: str,
                      object_to_upload: requests.Response | List[io.BytesIO],
                      s3_client: S3Client,
                      metadata: dict | None = None
                      ) -> bool:

    extra_args = {'Metadata': metadata} if metadata else {}
    to_upload: List[tuple[str, Any]] = []

    if isinstance(object_to_upload, requests.Response):
        if object_to_upload.raw:
            to_upload.append((file_name, object_to_upload.raw))

        
    elif isinstance(object_to_upload, list):
        for i, buffer in enumerate(object_to_upload):
            to_upload.append((f"{file_name}/chunk_{i + 1}.tif", buffer))

    else:
        raise ValueError(f"Expected requests.Response or List[io.BytesIO] as input. Got: {type(object_to_upload)}.")
    

    for key, fileobj in to_upload:
        s3_client.upload_fileobj(Bucket = bucket_name,
                                 Fileobj = fileobj,
                                 Key = key,
                                 ExtraArgs = extra_args)
        
    if metadata:
        metadata_content = json.dumps(metadata).encode('utf-8')
        s3_client.put_object(
                Bucket = bucket_name,
                Key = f"{file_name}/metadata.json",
                Body = metadata_content
                )

    return True
