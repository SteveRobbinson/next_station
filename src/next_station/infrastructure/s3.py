import logging
import requests
import json
import boto3
from mypy_boto3_s3 import S3Client
from .runner import runner
from next_station.schemas.worldpop import ApiMetadata, S3Etag
from typing import Any
import io
from next_station.core.exceptions.external import AWSServiceError
from next_station.core.config.settings import settings

logger = logging.getLogger(__name__)

def create_s3_client() -> S3Client:

    logger.info("Started creating S3 client")

    try:
        s3 = boto3.client('s3')
        s3.head_bucket(Bucket=settings.aws.s3_bucket_name)
        logger.info("Successfully created S3 client")
        return s3
    
    except Exception as err:
        raise AWSServiceError.from_exception(err) from err


def get_s3_object_metadata(s3client: S3Client,
                           aws_s3_path: str,
                           metadata_file_name: str = 'metadata.json'
                           ) -> dict:

    logger.info(f"Retrieving metadata from {aws_s3_path}")

    try:
        aws_response = s3client.get_object(
            Bucket = aws_s3_path,
            Key = metadata_file_name)

        metadata = json.load(aws_response['Body'])
        ### model pydantic, walidacja schematu json, do zrobienia
        logger.info(f"Successfully retrieved metadata from {aws_s3_path}/{metadata_file_name}")
        return metadata

    
    except Exception as err:
        raise AWSServiceError.from_exception(err) from err


def compare_metadata(s3_metadata: dict,
                     file_url: str
                    ) -> bool:
    
    logger.info(f"Comparing metadata for {file_url}")

    if not s3_metadata:
        logger.warning(f"Comparison aborted: No metadata available for {file_url}")
        return False

    try:
        api_response = runner(file_url, 'head')
        api_etag = ApiMetadata(**api_response.headers).etag
        aws_s3_etag = S3Etag(**s3_metadata).s3_etag

        is_match = aws_s3_etag == api_etag
        logger.info(f"Metadata match for {file_url}: {is_match}")
        return is_match
    

    except Exception as err:
        # Tutaj musze uzyc UnifiedAPIError zamiast AWSServiceError
        raise AWSServiceError.from_exception(err) from err


def upload_data_to_s3(bucket_name: str,
                      file_name: str,
                      object_to_upload: requests.Response | list[io.BytesIO],
                      s3_client: S3Client,
                      metadata: dict | None = None
                      ) -> bool:

    logger.info(f"Starting uploading {file_name} to bucket {bucket_name}")
    extra_args = {'Metadata': metadata} if metadata else {}
    to_upload: list[tuple[str, Any]] = []

    try:
        if isinstance(object_to_upload, requests.Response):
            if object_to_upload.raw:
                logger.info(f"Detected requests.Response as input for {file_name}")
                to_upload.append((file_name, object_to_upload.raw))

        elif isinstance(object_to_upload, list):
            logger.info(f"Detected list of io.BytesIO as input ({len(object_to_upload)} chunks) for {file_name}")
            for i, buffer in enumerate(object_to_upload):
                to_upload.append((f"{file_name}/chunk_{i + 1}.tif", buffer))

        if not to_upload:
            msg = f"Input was valid type {type(object_to_upload)} but contained no data to upload"
            logger.warning(msg)
            raise ValueError(msg)
        

        for key, fileobj in to_upload:
            logger.info(f"Uploading object to S3: {key}")
            s3_client.upload_fileobj(Bucket = bucket_name,
                                     Fileobj = fileobj,
                                     Key = key,
                                     ExtraArgs = extra_args)
            
        if metadata:
            metadata_content = json.dumps(metadata).encode('utf-8')
            metadata_key = f"{file_name}/metadata.json"
            logger.info(f"Uploading metadata file to S3: {metadata_key}")
            s3_client.put_object(
                    Bucket = bucket_name,
                    Key = metadata_key,
                    Body = metadata_content
                    )

        logger.info(f"Successfully finished all upload operations for {file_name}")
        return True

    except Exception as err:
        logger.exception(f"Critical failure during S3 upload of {file_name}")
        raise AWSServiceError.from_exception(err) from err
