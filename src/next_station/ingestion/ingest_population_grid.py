import boto3
from .create_s3_client import create_s3_client
from src.next_station.config import settings
from .get_s3_object_metadata import get_s3_object_metadata
from .compare_metadata import compare_metadata
from src.next_station.schemas.worldpop import ApiMetadata
from .get_file_url import get_file_url
from .fetch_population_grid import fetch_population_grid
from .upload_data_to_s3 import upload_data_to_s3
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

s3 = create_s3_client()

population_grid_file_url = get_file_url(settings.population_grid_url)

s3_object_metadata = get_s3_object_metadata(s3,
                                            settings.aws_bucket_name,
                                            settings.aws_grid_file_name)

is_metadata_same = compare_metadata(s3_object_metadata, population_grid_file_url)


if not is_metadata_same:
    logger.info(f"Metadata mismatch for {settings.aws_grid_file_name}. Downloading new dataset...")

    population_grid = fetch_population_grid(population_grid_file_url)

    metadata = {'ETag': ApiMetadata(**population_grid.headers).etag}

    upload_data_to_s3(settings.aws_bucket_name,
                      settings.aws_grid_file_name,
                      population_grid,
                      s3,
                      metadata)
    
    logger.info(f"Successfully updated dataset: {settings.aws_grid_file_name}")

else:
    logger.info(f"Dataset {aws.grid_file_name} is up-to-date. Skipping download")

 
