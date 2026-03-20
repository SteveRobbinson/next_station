from .runner import runner
import requests

def fetch_train_stations(api_url: str,
                         query: str
                         ) -> requests.Response:

    return runner(api_url, 'post', stream=True, query=query)
