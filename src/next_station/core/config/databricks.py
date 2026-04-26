from pydantic import BaseModel, computed_field

class DatabricksConfig(BaseModel):
    compute_config: str = 'python-dev'
    catalog: str = 'main'
    schema_bronze: str
    schema_silver: str
    railway_stations_bronze_table: str = 'railway_stations'
    railway_stations_silver_table: str = 'int_railway_stations_h3'
    population_grid_bronze_table: str = 'population_grid'
    population_grid_silver_table: str = 'int_population_grid_h3'

    @computed_field # type: ignore[prop-decorator]
    @property
    def railway_stations_bronze_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_bronze}.{self.railway_stations_bronze_table}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def population_grid_bronze_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_bronze}.{self.population_grid_bronze_table}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def population_grid_silver_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_silver}.{self.population_grid_silver_table}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def railway_stations_silver_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_silver}.{self.railway_stations_silver_table}"

