from pydantic import BaseModel, computed_field

class AWSConfig(BaseModel):
    s3_protocol: str = 's3://'
    s3_bucket_name: str
    s3_railway_stations_file_name: str
    s3_population_grid_file_name: str
    railway_file_explode_by: str = 'elements'
    s3_public_prefix: str = 'public'

    @computed_field # type: ignore[prop-decorator]
    @property   
    def railway_stations_uri(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_railway_stations_file_name}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def population_grid_uri(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_population_grid_file_name}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def population_grid_public(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_public_prefix}/{self.s3_population_grid_file_name}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def railway_stations_public(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_public_prefix}/{self.s3_railway_stations_file_name}"

