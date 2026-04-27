from next_station.providers.fetch_railway_stations import fetch_train_stations
from next_station.core.config.settings import settings
from next_station.infrastructure.s3 import create_s3_client, upload_data_to_s3

s3 = create_s3_client()

train_stations = fetch_train_stations(str(settings.api.base_railway_stations_url),
                                      settings.api.payload_for_railway_stations)

upload_data_to_s3(settings.aws.s3_bucket_name,
                  settings.aws.s3_railway_stations_file_name,
                  train_stations,
                  s3)
