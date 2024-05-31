from typing import Iterator
from models.common.io import InputReader
from .string_transform import StringTransform, Spin, Exchange, Partner


def _parse_string_transformer(instruction: str) -> StringTransform:
    if instruction.startswith("s"):
        return Spin(int(instruction[1:]))
    elif instruction.startswith("x"):
        parts = instruction[1:].split("/")
        return Exchange(int(parts[0]), int(parts[1]))
    elif instruction.startswith("p"):
        parts = instruction[1:].split("/")
        return Partner(parts[0], parts[1])


def parse_string_transformers(input_reader: InputReader) -> Iterator[StringTransform]:
    for instruction in input_reader.read().split(","):
        yield _parse_string_transformer(instruction.strip())
