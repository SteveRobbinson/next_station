import logging
from next_station.infrastructure.runner import runner
from next_station.schemas.worldpop import GetFileUrl
from next_station.core.exceptions.external import APIResponseError

logger = logging.getLogger(__name__)

def get_file_url(api_url: str,
                 index: int = -1,
                 redirect = True
                 ) -> str:
    
    logger.info(f"Retrieving file_url from {api_url}")

    try:

        response = runner(api_url, 'get', redirect=redirect)
        response = response.json()
        result = GetFileUrl(**response)

        logger.info(f"Successfully retrieved file url from {api_url}")
        return result[index]


    except Exception as err:
       logger.exception(f"Critical error during file URL retrieval from {api_url}")
       raise APIResponseError(response) from err
