from typing import Iterator
from models.common.io import InputReader
from .reindeer import Reindeer


def _parse_reindeer(reindeer_str: str) -> Reindeer:
    sentence_parts = reindeer_str.split(" ")
    return Reindeer(
        flight_speed=int(sentence_parts[3]),
        flight_interval=int(sentence_parts[6]),
        rest_interval=int(sentence_parts[13]),
    )


def parse_reindeers(input_reader: InputReader) -> Iterator[Reindeer]:
    for line in input_reader.read_stripped_lines():
        yield _parse_reindeer(line)
