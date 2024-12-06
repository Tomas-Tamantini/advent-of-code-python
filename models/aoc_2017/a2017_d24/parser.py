from typing import Iterator

from models.common.io import InputReader

from .bridge_builder import BridgeComponent


def parse_bridge_components(input_reader: InputReader) -> Iterator[BridgeComponent]:
    for line in input_reader.readlines():
        yield BridgeComponent(*map(int, line.strip().split("/")))
