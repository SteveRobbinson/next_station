import requests
from schemas.worldpop import ApiMetadata

def upload_data_to_s3(bucket_name: str,
                      file_name: str,
                      object_to_upload: requests.Resonse
                      ) -> bool:

    s3.upload_fileobj(Bucket = bucket_name,
                      Fileobj = object_to_upload.raw,
                      Key = file_name,
                      Metadata = {'ETag': ApiMetadata(**object_to_upload.headers).api_metadata})

    return True
