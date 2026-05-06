import logging
from next_station.core.spark import get_spark_session
from next_station.infrastructure.load_population_grid import load_population_grid
from next_station.core.config.settings import settings
from next_station.infrastructure.databricks import save_df_in_db
from sedona.spark import SedonaContext
from next_station.quality.extract_population_grid import extract_population_points
from next_station.core.exceptions.base import BaseAppError, InfrastructureError, UnifiedAPIError

logger = logging.getLogger(__name__)

def load_population_grid_to_databricks():
    logger.info('Initiating population grid load to Databricks Bronze layer')

    try:

        spark_session = get_spark_session(settings.databricks.compute_config)
        spark_session = SedonaContext.create(spark_session)

        logger.info(f"Ingesting raw data from {settings.aws.population_grid_uri}")
        raw_df = load_population_grid(spark_session, settings.aws.population_grid_uri)

        logger.info("Extracting population points from raw dataset")
        df_exploded = extract_population_points(raw_df)
    
        logger.info(f"Persisting exploded dataset to table: {settings.databricks.population_grid_bronze_fqn}")
        save_df_in_db(df_exploded, settings.databricks.population_grid_bronze_fqn)

        logger.info("Successfully completed population grid load to Databricks")    


    except (InfrastructureError, UnifiedAPIError) as known_err:

        logger.error(f"Job failed due to error in {known_err.source}: {known_err.details}")
        raise


    except Exception as err:

        msg = "Unexpected failure during Databricks population grid ingestion"
        logger.exception(msg)
        raise BaseAppError(
            source="PopulationGridDatabricksLoader",
            status_code=500,
            details=f"{msg}: {str(err)}"
        ) from err


if __name__ == '__main__':
    load_population_grid_to_databricks()
