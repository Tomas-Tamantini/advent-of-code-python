from typing import Iterator
from models.common.io import InputReader
from .logic import InitializationStep, RemoveLens, InsertLens


def _parse_initialization_step(step_str: str) -> InitializationStep:
    if "-" in step_str:
        return RemoveLens(label=step_str.split("-")[0])
    else:
        parts = step_str.split("=")
        return InsertLens(label=parts[0], focal_strength=int(parts[1]))


def parse_initialization_steps(
    input_reader: InputReader,
) -> Iterator[InitializationStep]:
    for step_str in input_reader.read().split(","):
        yield _parse_initialization_step(step_str)
