from enum import StrEnum

PACKAGE_NAME = 'next_station.core.data'
ERROR_MAPPING_FILE = 'error_mappings.json'

class ErrorCategory(StrEnum):
    STATUS_DESC = 'status_description'
    AWS_TO_HTTP = 'aws_error_to_status'
