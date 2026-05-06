import logging
from next_station.core.spark import get_spark_session
from next_station.infrastructure.load_railway_stations import load_json_source
from next_station.quality.df_empty import is_df_empty
from next_station.quality.melt_table import melt_table
from next_station.core.config.settings import settings
from next_station.infrastructure.databricks import save_df_in_db
from next_station.core.config.base import ComputeMode
from next_station.core.exceptions.base import BaseAppError, InfrastructureError, UnifiedAPIError

logger = logging.getLogger(__name__)

def load_railway_stations_to_databricks():
    logger.info('Initiating railway stations load to Databricks Bronze layer')

    try:

        config = settings.load_compute_config(ComputeMode.SQL) 
        spark_session = get_spark_session(config.databricks.compute_config)

        logger.info(f"Ingesting raw data from {settings.aws.railway_stations_uri}")
        df = load_json_source(spark_session, settings.aws.railway_stations_uri)

        logger.info(f"Exploding table by {settings.aws.railway_file_explode_by}")
        df = melt_table(df, settings.aws.railway_file_explode_by)

        logger.info("Integrity checks...")
        df = is_df_empty(df)

        logger.info(f"Persisting dataset to table {settings.databricks.railway_stations_bronze_fqn}")
        save_df_in_db(df, settings.databricks.railway_stations_bronze_fqn)

        logger.info("Successfully loaded railway stations to Databricks")


    except (InfrastructureError, UnifiedAPIError) as known_err:

            logger.error(f"Job failed due to error in {known_err.source}: {known_err.details}")
            raise


    except Exception as err:

        msg = "Unexpected failure during Databricks railway stations ingestion"
        logger.exception(msg)
        raise BaseAppError(
            source="### RailwayStationsDatabricksLoader ###",
            status_code=500,
            details=f"{msg}: {str(err)}"
        ) from err


if __name__ == '__main__':
    load_railway_stations_to_databricks()
