import requests
from requests.exceptions import HTTPError
import time

def fetch_train_stations(api_url: str,
                         query: str):

    max_retries = 3

    # Create a loop to handle temporary errors, ensure successful API response
    for i in range(max_retries):
        
        try: 
            response = requests.post(
                url = api_url,
                data = query
            )
            
            response.raise_for_status()

            # If response is a success, then break the loop
            break
            
        except HTTPError:
            
            # Error handling, if status code is 400 (Bad Request), we'll break the loop and print error message
            if response.status_code == 400:
                print(f"Failed!: \n{response.text}")

                raise

            # Handling temporary errors and retry
            if response.status_code in (429, 500, 501, 502, 503, 504):
                   
                time.sleep((i + 1) * 4) # We'll wait more with each iteration
                continue

            response.raise_for_status()

        # Handling other errors, function returns error message and then breaks
        except Exception as err:
            print(f"Other error occurred: {err}")

            raise 

    return response.json()
