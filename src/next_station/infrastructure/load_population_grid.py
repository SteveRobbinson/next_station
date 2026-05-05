import logging
from pyspark.sql import SparkSession, DataFrame
from next_station.core.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)

def load_population_grid(spark: SparkSession,
                         aws_s3_path: str,
                         data_format: str = 'binaryFile') -> DataFrame:

    logger.info(f"Starting loading population grid from {aws_s3_path}")

    try:
        df =spark.read.format(data_format).option("pathGlobFilter", "*.tif").load(aws_s3_path)

        logger.info(f"Successfully loaded population grid file from {aws_s3_path}")
        return df


    except Exception as err:
        logger.exception(f"Error occurred while loading population grid file from {aws_s3_path}")
        raise InfrastructureError(
            source="### Spark Population Grid Loader ###",
            status_code=500,
            details=f"Failed to load binary data (*.tif): {str(err)}"
        ) from err
