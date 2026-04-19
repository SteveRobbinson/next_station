from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, BaseModel, computed_field
from enum import Enum


class ComputeMode(str, Enum):
    SQL = 'sql'
    PYTHON = 'python'


class DatabricksConfig(BaseModel):
    compute_config: str = 'python'
    catalog: str = 'main'
    schema_name: str
    railway_stations_table: str = 'railway_stations'
    population_grid_table: str = 'population_grid'

    @property
    @computed_field
    def railway_stations_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_name}.{self.railway_stations_table}"

    @property
    @computed_field
    def population_grid_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_name}.{self.population_grid_table}"


class AWSConfig(BaseModel):
    s3_protocol: str = 's3://'
    s3_bucket_name: str
    s3_railway_stations_file_name: str
    s3_population_grid_file_name: str
    railway_file_explode_by: str = 'elements'

    @property
    @computed_field
    def railway_stations_uri(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_railway_stations_file_name}"

    @property
    @computed_field
    def population_grid_uri(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_population_grid_file_name}"


class ApiRequestsConfig(BaseModel):
    allowed_methods: set[str] = {'GET', 'HEAD', 'POST'}

    base_railway_stations_url: HttpUrl
    payload_for_railway_stations: str

    base_population_grid_url: HttpUrl


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_nested_delimiter='__')
    
    databricks: DatabricksConfig
    aws: AWSConfig
    api: ApiRequestsConfig


    @classmethod
    def load_compute_config(cls, mode: ComputeMode):
        configs = {
                ComputeMode.SQL: 'sql-dev',
                ComputeMode.PYTHON: 'python-dev'
                }

        return cls(databricks={'compute_config': configs[mode]}) # type: ignore

settings = AppConfig() # type: ignore
