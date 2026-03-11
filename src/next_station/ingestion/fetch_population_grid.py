from .runner import runner
import jsonpath

def fetch_population_grid(api_url: str,
                          json_expr: str
                          ) -> bool:

    response = runner(api_url, 'get')

    if response is not None:

        try:

            file_url = jsonpath.findall(json_expr, response.json())
            population_grid = runner(*file_url, 'get')

            if population_grid:
                
                with open('population_grid.tif', 'wb') as file:
                    file.write(population_grid.content)

                    return True


        except TypeError as err:
            print(f"List is either empty or got too many arguments \n{err}")

        except OSError as oserr:
            print(f"Error occurred while writing file on disk \n{oserr}")

        except Exception as ex:
            print(f"Other error occurred: \n{ex}")


    return False
