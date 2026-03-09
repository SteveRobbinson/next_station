import requests
from .runner import runner

def fetch_train_stations(api_url: str,
                         query: str
                         ) -> dict | None:

    response = runner(api_url, 'post', query)

    if response is not None:
        return response.json()

    return None
