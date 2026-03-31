import requests
from src.next_station.schemas.worldpop import ApiMetadata
from mypy_boto3_s3 import S3Client

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
