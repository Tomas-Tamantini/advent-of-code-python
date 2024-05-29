import json
from typing import Optional


def sum_all_numbers_in_json(
    json_str: str, property_to_ignore: Optional[str] = None
) -> int:
    parsed_json = json.loads(json_str)
    return _sum_numbers_in_json_recursive(parsed_json, property_to_ignore)


def _sum_numbers_in_json_recursive(
    json_object: dict | list | str | int,
    property_to_ignore: Optional[str],
) -> int:
    if isinstance(json_object, str):
        return 0
    if isinstance(json_object, int):
        return json_object
    if isinstance(json_object, list):
        return sum(
            _sum_numbers_in_json_recursive(obj, property_to_ignore)
            for obj in json_object
        )
    if isinstance(json_object, dict):
        if (
            property_to_ignore is not None
            and property_to_ignore in json_object.values()
        ):
            return 0
        return sum(
            _sum_numbers_in_json_recursive(obj, property_to_ignore)
            for obj in json_object.values()
        )
    raise ValueError("Invalid json format")
