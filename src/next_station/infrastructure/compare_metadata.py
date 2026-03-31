from .runner import runner
from src.next_station.schemas.worldpop import ApiMetadata, S3Etag
from pydantic import ValidationError

def compare_metadata(s3_metadata: dict,
                     file_url: str
                    ) -> bool:

    try:

        api_response = runner(file_url, 'head')
        api_etag = ApiMetadata(**api_response.headers).etag

        aws_s3_etag = S3Etag(**s3_metadata).s3_etag

        return aws_s3_etag == api_etag
    
    except ValidationError:
        return False
