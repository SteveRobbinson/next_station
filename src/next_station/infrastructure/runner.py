import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
import time
from src.next_station.core.config import settings
from src.next_station.core.exceptions import (
        ApiRequestError,
        ApiUnauthorizedError,
        ApiForbiddenRequestError,
        ApiConnectionError,
        ApiRateLimitError,
        ApiUnhandledError,
        ApiTimeoutError
        )
from src.next_station.infrastructure.utils import _perform_backoff

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
            
        except (Timeout, ConnectionError) as err:

            if i == max_retries - 1:
                raise ApiTimeoutError(f"Final attempt {i+1} failed for {api_url}") from err

            _perform_backoff(i)
            continue

        except HTTPError as err:
            
            if response.status_code in (400, 404):
                raise ApiRequestError(response) from err

            elif response.status_code == 401:
                raise ApiUnauthorizedError(response) from err

            elif response.status_code == 403:
                raise ApiForbiddenRequestError(response) from err

            elif response.status_code in (429, 500, 501, 502, 503, 504):
                if i == max_retries - 1:
                    
                    if response.status_code == 429:
                        raise ApiRateLimitError(response) from err

                    else:
                        raise ApiConnectionError(response) from err

                _perform_backoff(i)
                continue

            else:
                raise ApiUnhandledError(response) from err

    raise RuntimeError("Unhandled error occured! Try again")
