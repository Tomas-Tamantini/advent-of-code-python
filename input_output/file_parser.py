from models.a2015_d2 import XmasPresent
from typing import Iterator


def parse_xmas_presents(file_name: str) -> Iterator[XmasPresent]:
    with open(file_name, "r") as f:
        for line in f:
            yield XmasPresent(*map(int, line.split("x")))
