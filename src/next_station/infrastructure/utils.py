import logging
import time
from next_station.core.exceptions.base import InfrastructureError
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)

def _perform_backoff(current_retry_count: int,
                     base_delay: int = 1,
                     backoff_factor: int = 5,
                     max_delay: int = 60):

    delay = base_delay + (backoff_factor ** current_retry_count)
    sleep_time = min(delay, max_delay)

    time.sleep(sleep_time)


def consolidate_to_single_parquet(spark: SparkSession,
                                  source_fqn: str,
                                  aws_bucket_uri: str):
    
    logger.info(f"Consolidating table {source_fqn} into a single parquet file at {aws_bucket_uri}")

    try:
        df = spark.table(source_fqn)
        
        (df.repartition(1)
         .write
         .mode('overwrite')
         .format('parquet')
         .save(aws_bucket_uri))
        logger.info(f"Successfully consolidated {source_fqn} into {aws_bucket_uri}")


    except Exception as err:
        logger.exception(f"REPARTITION(1) FAILURE: Could not consolidate table {source_fqn} to S3 destination {aws_bucket_uri}. Spark job aborted.")
        raise InfrastructureError(
                source="### Parquet Consolidator ###",
                status_code=500,
                details=f"Infrastructure failure: Data consolidation for {source_fqn} failed."
                ) from err
