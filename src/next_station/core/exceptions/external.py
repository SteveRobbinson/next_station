import requests
from typing import Self
from src.next_station.core.exceptions.base import UnifiedAPIError
from botocore.exceptions import BotoCoreError, ClientError
from next_station.core.resources import get_error_mapping
from next_station.core.constants import ErrorCategory

### API RESPONSE ###
class APIResponseError(UnifiedAPIError):
    source = '### API ###'

    def __init__(self, response: requests.Response):
        self.response = response
        status_code = int(getattr(response, 'status_code', 500))
        reason = getattr(response, 'reason', 'Unknown')

        super().__init__(self.source, status_code, details=reason)



class APITimeoutError(UnifiedAPIError):
    source = '### API TIMEOUT ###'

    def __init__(self, url: str, details: str):
        status_code = 504
        msg_details = f"Timeout for: {url}"

        if details:
            msg_details += f" | {details}"
            
        super().__init__(self.source, status_code, details=msg_details) 



### AWS SERVICE ERROR ###
class AWSServiceError(UnifiedAPIError):
    """Base class for AWS related errors"""
    
    def __init__(self, source, status_code: int, details: str):
        super().__init__(self.source, self.status_code, self.details)
    
    @classmethod
    def from_exception(cls, error: Exception) -> "Self | AWSConfigError | AWSResponseError":
        if isinstance(error, BotoCoreError):
            return AWSConfigError(error)

        if isinstance(error, ClientError):
            return AWSResponseError(error)

        return cls(source='AWS Unknown Error', status_code=500, details=str(error))



class AWSConfigError(AWSServiceError):
    source = '### AWS CONFIG ERROR ###'

    def __init__(self, error: BotoCoreError):
        self.error = error
        status_code = get_error_mapping(ErrorCategory.AWS_TO_HTTP, type(error).__name__, 500)

        super().__init__(self.source, status_code, str(error))



class AWSResponseError(AWSServiceError):
    source = '### AWS RESPONSE ERROR ###'
    aws_to_http = aws_response_errors
    
    def __init__(self, error: ClientError):
        self.error = error
        aws_code = error.response.get('Error', {}).get('Code', 'Unknown')
        status_code = self.aws_to_http.get(aws_code, 500)
    
        super().__init__(self.source, status_code, details=aws_code)  
