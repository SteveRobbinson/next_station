from pydantic import BaseModel, BeforeValidator, Field, ConfigDict, AliasChoices, AfterValidator
from typing import Annotated

def ensure_one_element(value: any) -> str:

    if isinstance(value, list):
        
        if len(value) != 1:
            raise ValueError(f"Expected one file url, got: {len(value)}.")
            
        else:
            return value[0]

    else:
        return value



class FileUrl(BaseModel):
    file_url: Annotated[str, BeforeValidator(ensure_one_element), Field(alias='files')]



class GetFileUrl(BaseModel):
    list_url: Annotated[list[FileUrl], Field(alias='data', min_length = 1)]

    def __getitem__(self, index):
        return self.list_url[index].file_url


### Extracting metadata/ETag from a api head request

def ensure_string(value: any) -> str:

    if isinstance(value, str):
        return value.strip().strip('"')

    else:
        return value


class ApiMetadata(BaseModel):
    model_dict = ConfigDict(populate_by_name=True)

    etag: Annotated[str,
                    Field(validation_alias=AliasChoices('ETag', 'etag', 'Etag')),
                    AfterValidator(ensure_string)]
