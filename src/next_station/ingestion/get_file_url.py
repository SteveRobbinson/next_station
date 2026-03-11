from .runner import runner
import jsonpath

def get_file_url(api_url:str,
                 json_expr:str
                 ) -> str:

    response = runner(api_url, 'get')
    list_files = jsonpath.findall(json_expr, response.json())

    if len(list_files) == 1:
        return list_files[0]

    else:
        raise ValueError(f"Expected one file url, got: {len(list_files)} file url's")

