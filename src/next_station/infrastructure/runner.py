import requests
from requests.exceptions import HTTPError
import time

def runner(api_url: str,
           method: str,
           stream: bool | None = None,
           query: str | None = None,
           max_retries: int = 3,
           timeout: int = 60
           ) -> requests.Response:

    for i in range(max_retries):
        
        try:

            if method == 'head':
                response = requests.head(url = api_url, params = query, allow_redirects = True, timeout = timeout)

            elif method == 'get':
                response = requests.get(url = api_url, allow_redirects = True, stream = stream, timeout = timeout)
            
            elif method == 'post':
                response = requests.post(url = api_url, data = query, stream = stream, timeout = timeout)
            
            response.raise_for_status()

            return response
            

        except HTTPError as err:
            
            if response.status_code in (400, 404):
                raise ValueError(f"WorldPop API - Invalid {method.upper()} request to {api_url}\nStatus code: {response.status_code}\nDetails: {response.text}") from err

            elif response.status_code in (429, 500, 501, 502, 503, 504):
                if i == max_retries - 1:
                    raise ConnectionError(f"WorldPop API - Max retries reached. Status code: {response.status_code}\nDetails: {response.text}") from err

                time.sleep((i + 1) * 4)
                continue

            raise RunTimeError(f"WorldPop API - Unhandled HTTPError: {response.status_code}\nDetails: {response.text}") from err
