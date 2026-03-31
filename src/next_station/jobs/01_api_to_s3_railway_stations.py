from src.next_station.ingestion.fetch_train_stations import fetch_train_stations
from src.next_station.config import settings
from src.next_station.ingestion.upload_data_to_s3 import upload_data_to_s3
from src.next_station.ingestion.create_s3_client import create_s3_client
import boto3
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger.info("Starting train stations ingestion process...")
s3 = create_s3_client()

logger.info(f"Fetching train stations from API: {settings.train_stations_url}")
train_stations = fetch_train_stations(settings.train_stations_url,
                                      settings.query_for_train_stations)

logger.info(f"Uploading train stations data to S3 bucket: {settings.aws_bucket_name}")
upload_data_to_s3(settings.aws_bucket_name,
                  settings.aws_train_file_name,
                  train_stations,
                  s3)

logger.info("Train stations ingestion completed successfully.")
