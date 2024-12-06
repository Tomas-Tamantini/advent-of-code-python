from typing import Iterator

from models.common.io import InputReader


def parse_passports(input_reader: InputReader) -> Iterator[dict[str, str]]:
    passport = {}
    for line in input_reader.read_stripped_lines(keep_empty_lines=True):
        if line:
            parts = line.split()
            for part in parts:
                key, value = part.split(":")
                passport[key] = value
        else:
            if passport:
                yield passport
            passport = {}
    if passport:
        yield passport
