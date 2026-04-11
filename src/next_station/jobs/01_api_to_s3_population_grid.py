import boto3
from src.next_station.infrastructure.s3 import (
    create_s3_client,
    get_s3_object_metadata,
    compare_metadata,
    upload_data_to_s3
)

from src.next_station.core.config import settings
from src.next_station.schemas.worldpop import ApiMetadata
from src.next_station.providers.get_file_url import get_file_url
from src.next_station.providers.fetch_population_grid import fetch_population_grid
import logging
from src.next_station.infrastructure.slice_dataset import slice_dataset

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

s3 = create_s3_client()

population_grid_file_url = get_file_url(settings.population_grid_url)

s3_object_metadata = get_s3_object_metadata(s3,
                                            settings.aws_bucket_name,
                                            settings.aws_population_grid_metadata_file)

is_metadata_same = compare_metadata(s3_object_metadata, population_grid_file_url)


if not is_metadata_same:
    logger.info(f"Metadata mismatch for {settings.aws_population_grid_file_name}. Downloading new dataset...")

    population_grid = fetch_population_grid(population_grid_file_url)

    metadata = {'ETag': ApiMetadata(**population_grid.headers).etag}
    
    sliced_dataset = slice_dataset(population_grid)

    upload_data_to_s3(settings.aws_bucket_name,
                      settings.aws_population_grid_file_name,
                      sliced_dataset,
                      s3,
                      metadata)
    
    logger.info(f"Successfully updated dataset: {settings.aws_population_grid_file_name}")

else:
    logger.info(f"Dataset {aws.population_grid_file_name} is up-to-date. Skipping download")
