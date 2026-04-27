from next_station.infrastructure.s3 import (
    create_s3_client,
    get_s3_object_metadata,
    compare_metadata,
    upload_data_to_s3
)
from next_station.core.config.settings import settings
from next_station.schemas.worldpop import ApiMetadata
from next_station.providers.get_file_url import get_file_url
from next_station.providers.fetch_population_grid import fetch_population_grid
from next_station.infrastructure.slice_dataset import slice_dataset

s3 = create_s3_client()

population_grid_file_url = get_file_url(str(settings.api.base_population_grid_url))

s3_object_metadata = get_s3_object_metadata(s3,
                                            settings.aws.s3_bucket_name)

is_metadata_same = compare_metadata(s3_object_metadata, population_grid_file_url)


if not is_metadata_same:

    population_grid = fetch_population_grid(population_grid_file_url)

    metadata = {'ETag': ApiMetadata(**population_grid.headers).etag}
    
    sliced_dataset = slice_dataset(population_grid)

    upload_data_to_s3(settings.aws.s3_bucket_name,
                      settings.aws.s3_population_grid_file_name,
                      sliced_dataset,
                      s3,
                      metadata)
