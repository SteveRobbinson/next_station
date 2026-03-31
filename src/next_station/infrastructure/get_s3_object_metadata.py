import boto3
from mypy_boto3_s3 import S3Client
from botocore.exceptions import ClientError
from src.next_station.ingestion.exceptions import S3ServiceError, S3AccessDeniedError, S3NotFoundError

def get_s3_object_metadata(s3client: S3Client,
                           bucket_name: str,
                           file_name_on_s3: str
                           ) -> dict:

    try:
        
        aws_response = s3client.head_object(
            Bucket = bucket_name,
            Key = file_name_on_s3)

        return aws_response

    
    except ClientError as ce:
        

        status_code = ce.response['Error']['Code']
        
        if status_code == '403':
            raise S3AccessDeniedError(f"AWS S3 - Access denied. Status code: {status_code}\nProvided credentials do not have permissions to access S3 resources") from ce

        elif status_code == '404':
            raise S3NotFoundError(f"AWS S3 - File or bucket not found. Status code: {status_code}") from ce

        else:
            raise S3ServiceError(f"AWS S3 - Client Error occurred! Status code: {status_code}") from ce
