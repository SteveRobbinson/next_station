import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, NoRegionError, EndpointConnectionError

def fetch_s3_client(bucket_name: str,
                    file_name_on_s3: str
                    ) -> dict:

    try:
        
        s3 = boto3.client('s3')
        aws_response = s3.head_object(
            Bucket = bucket_name,
            Key = file_name_on_s3
        )

        return aws_response

    
    except ClientError as ce:
        

        status_code = ce.response['Error']['Code']
        
        if status_code == '403':
            raise ClientError(f"AWS S3 - Access denied. Status code: {status_code}\nProvided credentials do not have permissions to access S3 resources") from ce

        else:
            raise ClientError(f"AWS S3 - Client Error occured! Status code: {status_code}") from ce


    except (NoCredentialsError, PartialCredentialsError) as nce:
        raise NoCredentialsError(f"AWS S3 - No credentials found. Check your AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY") from nce


    except NoRegionError as nre:
        raise NoRegionError(f"AWS S3 - Region for client S3 not specified!") from nre


    except EndpointConnectionError as ece:
        raise EndpointConnectionError(f"AWS S3 - Could not connect to the endpoint. Please check your internet or AWS service status") from ece
