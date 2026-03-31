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
