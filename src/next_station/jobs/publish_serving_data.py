from next_station.core.spark import get_spark_session
from next_station.core.config.settings import settings
from next_station.infrastructure.utils import consolidate_to_single_parquet

spark = get_spark_session(settings.databricks.compute_config)

for task in settings.export_tasks:
    consolidate_to_single_parquet(spark,
                                  source_fqn = task.databricks_fqn,
                                  aws_bucket_uri = task.aws_target_uri)
