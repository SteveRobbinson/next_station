import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from src.next_station.core.config import settings
from src.next_station.infrastructure.utils import _perform_backoff
from src.next_station.core.exceptions.external import APITimeoutError, APIResponseError
from src.next_station.core.exceptions.base import UnifiedAPIError

def runner(api_url: str,
           method: str,
           payload: str | None = None,
           stream: bool = False,
           redirect: bool = False,
           timeout: int = 60,
           max_retries: int = 3,
           **kwargs
           ) -> requests.Response:

    method = method.upper()

    if method not in settings.api.allowed_methods:
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
                raise APITimeoutError(api_url, str(err)) from err

            _perform_backoff(i)
            continue


        except HTTPError as err:
            status_code = err.response.status_code

            if status_code in [429, 500, 501, 502, 503, 504] and i < max_retries - 1:
                _perform_backoff(i)
                continue

            raise APIResponseError(response) from err

    raise UnifiedAPIError(source = '### API ###', status_code = 500, details = 'Unhandled retry logic failure')
