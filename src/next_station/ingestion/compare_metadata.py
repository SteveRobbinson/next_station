from .runner import runner
import boto3
from botocore.exceptions import ClientError

def compare_metadata(bucket_name: str,
                     file_name_on_s3:str,
                     file_url: str
                    ) -> bool:

    try:

        api_response = runner(file_url, 'head')

        s3 = boto3.client('s3')
        aws_response = s3.head_object(
            Bucket = bucket_name,
            Key = file_name_on_s3
        )

        aws_s3_metadata = aws_response['Metadata']['etag']
        api_metadata = api_response.headers['ETag'].strip('"')
        
        if aws_s3_metadata == api_metadata:
            return True

    
    except ClientError as e:

        if int(e.response['Error']['Code']) == 404:
            return False


    except (AttributeError, KeyErro) as err:
        print(f"Check if ETag exists at API response headers \n{err}")
    

    return False
