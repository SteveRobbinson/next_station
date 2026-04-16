from src.next_station.infrastructure.runner import runner
import requests

def fetch_train_stations(api_url: str,
                         payload: str
                         ) -> requests.Response:

    return runner(api_url, 'post', payload, stream=True)
