from pydantic import BaseModel
from enum import Enum

class ComputeMode(str, Enum):
    SQL = 'sql'
    PYTHON = 'python'


class ExportTask(BaseModel):
    name: str
    databricks_fqn: str
    aws_target_uri: str

