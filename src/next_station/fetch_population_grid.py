import requests

def fetch_population_grid(api_url: str) -> str | None:

    response = runner(api_url, 'get')

    if response is not None:

        file_url = response.json()['data'][-1].get('files')[0]
        population_grid = runner(file_url, 'get')

        
        if population_grid:
            
            with open('population_grid.tif', 'wb') as file:
                file.write(population_grid.content)

                return 'Success'

    return None     
