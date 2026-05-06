import logging
from next_station.core.spark import get_spark_session
from next_station.core.config.settings import settings
from next_station.infrastructure.utils import consolidate_to_single_parquet
from next_station.core.exceptions.base import BaseAppError, InfrastructureError, UnifiedAPIError

logger = logging.getLogger(__name__)

def run_export_job():
    tasks = settings.export_tasks
    logger.info(f"Starting export job for {len(tasks)} tasks")
    
    try:

        spark = get_spark_session(settings.databricks.compute_config)

        for task in settings.export_tasks:
            consolidate_to_single_parquet(spark,
                                          source_fqn = task.databricks_fqn,
                                          aws_bucket_uri = task.aws_target_uri)

        logger.info("All export tasks completed successfully")

            
    except (InfrastructureError, UnifiedAPIError) as known_err:

            logger.error(f"Export job aborted due to error in {known_err.source}: {known_err.details}")
            raise


    except Exception as err:

        msg = 'Unexpected failure in export loop'
        logger.exception(msg)
        raise BaseAppError(
            source="### DataExporterJob ###",
            status_code=500,
            details=f"{msg}: {str(err)}"
        ) from err


if __name__ == "__main__":
    run_export_job()
