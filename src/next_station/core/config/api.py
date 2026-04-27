from pydantic import BaseModel, HttpUrl

class ApiRequestsConfig(BaseModel):
    allowed_methods: set[str] = {'GET', 'HEAD', 'POST'}

    base_railway_stations_url: HttpUrl
    payload_for_railway_stations: str

    base_population_grid_url: HttpUrl
    headers: dict[str, str]

