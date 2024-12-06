from typing import Iterator

from models.common.io import InputReader

from .cookie import CookieProperties


def _parse_single_cookie_properties(properties_str: str) -> CookieProperties:
    parts = properties_str.replace(",", "").split(" ")
    return CookieProperties(
        capacity=int(parts[2]),
        durability=int(parts[4]),
        flavor=int(parts[6]),
        texture=int(parts[8]),
        calories=int(parts[10]),
    )


def parse_cookie_properties(input_reader: InputReader) -> Iterator[CookieProperties]:
    for line in input_reader.read_stripped_lines():
        yield _parse_single_cookie_properties(line)
