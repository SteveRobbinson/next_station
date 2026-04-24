import time
from pyspark.sql import SparkSession

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
    
    df = spark.table(source_fqn)

    (df.repartition(1)
     .write
     .mode('overwrite')
     .format('parquet')
     .save(aws_bucket_uri))
