from .runner import runner

def fetch_train_stations(api_url: str,
                         query: str
                         ) -> dict:

    return runner(api_url, 'post', query=query).json()
