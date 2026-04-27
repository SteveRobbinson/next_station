from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from next_station.core.config.databricks import DatabricksConfig
from next_station.core.config.aws import AWSConfig
from next_station.core.config.api import ApiRequestsConfig
from next_station.core.config.base import ComputeMode, ExportTask


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

    @computed_field # type: ignore[prop-decorator]
    @property
    def export_tasks(self) -> list[ExportTask]:

        return [
                ExportTask(name = 'population_grid',
                           databricks_fqn = self.databricks.population_grid_silver_fqn,
                           aws_target_uri = self.aws.population_grid_public
                           ),
                ExportTask(name = 'railway_stations',
                           databricks_fqn = self.databricks.railway_stations_silver_fqn,
                           aws_target_uri = self.aws.railway_stations_public)
                ]

settings = AppConfig() # type: ignore
