from importlib import resources
import json
from next_station.core.constants import PACKAGE_NAME, ERROR_MAPPING_FILE, ErrorCategory

def get_error_mapping(category: ErrorCategory, key: str | int, fallback: str | int) -> str | int:

    source = resources.files(PACKAGE_NAME).joinpath(ERROR_MAPPING_FILE)
    raw_data = source.read_text(encoding='utf-8')
    mappings = json.loads(raw_data)
    category_map = mappings.get(category, {})

    return category_map.get(str(key), fallback)
