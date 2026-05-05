import logging
from pyspark.sql import SparkSession, DataFrame
from next_station.core.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)

def load_json_source(spark: SparkSession,
                     aws_s3_path: str,
                     data_format: str = 'json'
                     ) -> DataFrame:

    logger.info(f"Started fetching railway stations from {aws_s3_path}")

    try:
        df = spark.read.format(data_format).option('multiLine', 'true').load(aws_s3_path)
        logger.info(f"Successfully loaded railway_stations from {aws_s3_path}")

        return df

    except Exception as err:
        logger.exception(f"Error occurred while loading railway stations from {aws_s3_path}")
        raise InfrastructureError(
            source="### Spark S3 Loader ###",
            status_code=500,
            details=f"Failed to load {data_format} source: {str(err)}"
        ) from err
