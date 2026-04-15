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
class ApiError(Exception):
    """Base class for API requests related errors """
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text

        message = f"API Error: {self.status_code}\n Details: {self.text[:200]}"
        super().__init__(message)

class ApiRequestError(ApiErrors):
    """Raised when the server can't process/find your request"""
    pass

class ApiUnauthorizedError(ApiErrors):
    """Raised when server rejected your request due to missing or invalid authentication."""
    pass

class ApiForbiddenRequest(ApiErrors):
    """Raised when server understood your request but denied access. Usually due to insufficient permissions."""
    pass

class ApiConnectionError(ApiErrors):
    """Raised when something broke on the hosting side"""
    pass

class ApiRateLimitError(ApiErrors):
    """Raised when you've sent too many requests in a short time."""
    pass

class ApiUnhandledError(ApiErrors):
    """Raised when an unhandled error occurs"""
    pass



