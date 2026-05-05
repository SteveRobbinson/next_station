import logging
from pyspark.sql import DataFrame
from next_station.core.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)

def save_df_in_db(df: DataFrame,
                  table_name: str,
                  save_format: str = 'delta',
                  save_mode: str = 'overwrite'):

    logger.info(f"Starting write to table: {table_name} (format: {save_format}, mode: {save_mode})")
    
    try:
        df.write.format(save_format).mode(save_mode).saveAsTable(table_name)
        logger.info(f"Table {table_name} saved successfully")


    except Exception as err:
        logger.exception(f"Error occurred while saving table {table_name} to databricks")
        raise InfrastructureError(
                source="### Spark Writer ###",
                status_code=500,
                details=f"Failed to persist table '{table_name}' using {save_format} format"
                ) from err
