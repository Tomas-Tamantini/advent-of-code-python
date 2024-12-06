from typing import Iterator

from models.common.io import InputReader

from .foods import Food


def _parse_food(line: str) -> Food:
    parts = line.split(" (contains ")
    ingredients = parts[0].split()
    allergens = parts[1].replace(")", "").split(", ")
    return Food(set(ingredients), set(allergens))


def parse_foods(input_reader: InputReader) -> Iterator[Food]:
    for line in input_reader.read_stripped_lines():
        yield _parse_food(line)
