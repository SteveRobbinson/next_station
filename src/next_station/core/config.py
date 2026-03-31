from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    train_stations_url: str
    population_grid_url: str
    query_for_train_stations: str
    aws_bucket_name: str
    aws_railway_stations_file_name: str
    aws_population_grid_file_name: str
    aws_s3_bucket_address: str
    aws_railway_file_explode_by: str
    databricks_catalog: str
    databricks_schema: str
    databricks_railway_table: str
    databricks_population_table: str

settings = Settings()
