import requests

# S3 errors
class S3ServiceError(Exception):
    """Base class for S3 related errors."""
    pass


class S3ConfigError(S3ServiceError):
    """Raised when AWS credentials or region are missing/invalid."""
    pass


class S3ConnectionError(S3ServiceError):
    """Raised when there is a network issue connecting to AWS."""
    pass


class S3AccessDeniedError(S3ServiceError):
    """Raised when the provided credentials lack permissions (403)."""
    pass


class S3NotFoundError(S3ServiceError):
    """Raised when the S3 object or bucket does not exist (404)."""
    pass

# API Errors
class BaseApiError(Exception):
    """Base class for API exceptions"""
    pass

class ApiError(BaseApiError):
    """Base class for API requests related errors """
    def __init__(self, response: requests.Response, title: str ='API Error'):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text

        message = f"{title}. Status code: {self.status_code}\nDetails: {self.text[:200]}"
        super().__init__(message)

class ApiRequestError(ApiError):
    """Raised when the server can't process/find your request"""
    def __init__(self, response):
        super().__init__(response, title="Server couldn't find/process your request!")


class ApiUnauthorizedError(ApiError):
    """Raised when server rejected your request due to missing or invalid authentication."""
    def __init__(self, response):
        super().__init__(response, title="The server rejected your request due to missing or invalid authentication")


class ApiForbiddenRequestError(ApiError):
    """Raised when server understood your request but denied access. Usually due to insufficient permissions."""
    def __init__(self, response):
        super().__init__(response, title="Access denied!")


class ApiConnectionError(ApiError):
    """Raised when something broke on the hosting side"""
    def __init__(self, response):
        super().__init__(response, title="An error occured on the hosting side!")


class ApiRateLimitError(ApiError):
    """Raised when you've sent too many requests in a short time."""
    def __init__(self, response):
        super().__init__(response, title="Too many requests sent!")


class ApiUnhandledError(ApiError):
    """Raised when an unhandled error occurs"""
    def __init__(self, response):
        super().__init__(response, title="An unhandled error occured!")

class ApiTimeoutError(BaseApiError):
    def __init__(self, message: str = "The request timed out!"):
        super().__init__(message)
