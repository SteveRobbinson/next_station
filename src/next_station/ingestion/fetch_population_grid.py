from .runner import runner
import requests

def fetch_population_grid(api_url: str) -> requests.Response:

    return runner(api_url, 'get', stream=True)
