import requests
from botocore.exceptions import (
        BotoCoreError,
        ClientError,
        NoCredentialsError,
        NoRegionError,
        UnknownServiceError,
        EndpointConnectionError,
        ReadTimeoutError,
        ConnectTimeoutError,
        ProxyConnectionError,
        SSLError,
        CredentialRetrievalError
        )
from typing import Self

# S3 errors
class S3ServiceError(Exception):
    """Base class for S3 related errors."""
    
    @classmethod
    def from_exception(cls, error: Exception) -> "Self | S3ConfigError":
        
        if isinstance(error, BotoCoreError):
            return S3ConfigError(error)

        if isinstance(error, ClientError):
            code = error.response.get('Error', {}).get('Code', 'Unknown')
            message = f"AWS S3 Server Error [{code}]: {error}"

        else:
            message = f"An unexpected error occurred during AWS S3 initialization! {error}"

        return cls(message)


class S3ConfigError(S3ServiceError):
    """Raised when AWS credentials or region are missing/invalid."""

    error_map: dict[type[BotoCoreError], str] = {
            NoCredentialsError: "AWS S3 - No credentials found. Check your AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY",
            NoRegionError: "AWS S3 - Region for client S3 not specified!",
            UnknownServiceError: "AWS S3 - Incorrect service name!",
            EndpointConnectionError: "AWS S3 - Network connection error. Could not reach the service endpoint.",
            ReadTimeoutError: "AWS S3 - Read timeout occurred while receiving data from the server.",
            ConnectTimeoutError: "AWS S3 - Connection timeout. The server took too long to respond.",
            ProxyConnectionError: "AWS S3 - Proxy connection failed. Check your proxy settings.",
            SSLError: "AWS S3 - SSL certificate validation failed.",
            CredentialRetrievalError: "AWS S3 - Failed to retrieve credentials from the configured provider."
            }

    def __init__(self, error: BotoCoreError):
        self.error = error
        message = self.error_map.get(
                type(error), f"Configuration error occurred: {error}"
                )

        super().__init__(message)


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
