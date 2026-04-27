from next_station.infrastructure.runner import runner
from next_station.schemas.worldpop import GetFileUrl

def get_file_url(api_url: str,
                 index: int = -1,
                 redirect = True
                 ) -> str:

    response = runner(api_url, 'get', redirect=redirect)
    response = response.json()

    result = GetFileUrl(**response)

    return result[index]
