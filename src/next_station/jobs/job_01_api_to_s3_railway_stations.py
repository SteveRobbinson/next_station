import logging
from next_station.providers.fetch_railway_stations import fetch_train_stations
from next_station.core.config.settings import settings
from next_station.infrastructure.s3 import create_s3_client, upload_data_to_s3
from next_station.core.exceptions.base import BaseAppError, InfrastructureError, UnifiedAPIError

logger = logging.getLogger(__name__)

def ingest_railway_stations_to_s3():
    logger.info('Starting Railway Stations job')

    try:

        s3 = create_s3_client()
        train_stations = fetch_train_stations(str(settings.api.base_railway_stations_url), settings.api.payload_for_railway_stations)
        upload_data_to_s3(settings.aws.s3_bucket_name,
                          settings.aws.s3_railway_stations_file_name,
                          train_stations,
                          s3)

        logger.info('Successfully updated railway stations in S3.')


    except (InfrastructureError, UnifiedAPIError) as known_err:
        
        logger.error(f"Job failed due to known error in {known_err.source}: {known_err.details}")
        raise
        

    except Exception as err:

        msg = 'Unexpected failure in Railway Stations job'
        logger.exception(msg)
        raise BaseAppError(
            source="### RailwayStationsJob ###",
            status_code=500,
            details=f"{msg}: {str(err)}"
        ) from err


if __name__ == "__main__":
    ingest_railway_stations_to_s3()
