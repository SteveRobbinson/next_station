import logging
import requests
from next_station.core.exceptions.external import APIResponseError
from next_station.infrastructure.runner import runner

logger = logging.getLogger(__name__)

def fetch_population_grid(api_url: str) -> requests.Response:

    logger.info(f"Starting to fetch population grid dataset from {api_url}")
    
    try:
        response = runner(api_url, 'get', stream=True)

        logger.info(f"Successfully connected to population grid API. Status: {response.status_code}")
        return response


    except Exception as err:
        logger.exception(f"Failed to fetch population grid from {api_url}")
        raise APIResponseError(response) from err
