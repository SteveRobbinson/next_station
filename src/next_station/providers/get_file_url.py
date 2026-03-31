from .runner import runner
from src.next_station.schemas.worldpop import GetFileUrl, FileUrl

def get_file_url(api_url: str,
                 index: int = -1
                 ) -> str:

    response = runner(api_url, 'get')
    response = response.json()

    result = GetFileUrl(**response)

    return result[index]
