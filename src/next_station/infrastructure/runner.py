import requests
from requests.exceptions import HTTPError
import time
from src.next_station.core.config import settings
from src.next_station.core.exceptions import (
        ApiRequestError,
        ApiUnauthorizedError,
        ApiForbiddenRequest,
        ApiConnectionError,
        ApiRateLimitError,
        ApiUnhandledError
        )

def runner(api_url: str,
           method: str,
           payload: str | None,
           stream: bool | None,
           redirect: bool,
           timeout: int = 60,
           max_retries: int = 3,
           **kwargs
           ) -> requests.Response:

    method = method.upper()

    if method not in settings.allowed_methods:
        raise(ValueError(f"Method {method} is not supported. Check allowed_methods in config."))


    if max_retries <= 0:
        raise ValueError("Max retries must be a positive integer")


    if payload:

        if method in ('GET', 'HEAD'):
            kwargs.setdefault('params', payload)

        elif method == 'POST':
            kwargs.setdefault('data', payload)


    for i in range(max_retries):
        
        try:
                
            response = requests.request(method, url=api_url, allow_redirects=redirect, stream=stream, timeout=timeout, **kwargs)

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

    raise RuntimeError(f"WorldPop API - Unhandled HTTPError: {response.status_code}\nDetails: {response.text}") from err
