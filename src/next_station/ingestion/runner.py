import requests
from requests.exceptions import HTTPError
import time

def runner(api_url: str,
           method: str,
           stream: bool | None = None,
           query: str | None = None,
           max_retries: int = 3
           ) -> requests.Response | None:

    for i in range(max_retries):
        
        try:

            if method == 'head':
                response = requests.head(url = api_url, params = query, allow_redirects = True)

            elif method == 'get':
                response = requests.get(url = api_url, allow_redirects = True, stream = stream)
            
            elif method == 'post':
                response = requests.post(url = api_url, data = query, stream = stream)
            
            response.raise_for_status()

            return response
            

        except HTTPError:
            
            if response.status_code in (400, 404):
                print(f"Failed!: \n{response.text}")

                return None

            elif response.status_code in (429, 500, 501, 502, 503, 504):
                   
                time.sleep((i + 1) * 4)
                print(f"Status code: {response.status_code}, retrying...")
                continue


        except Exception as err:

            print(f"Other error occurred: {err}")

            return None

        return None
