from typing import Iterator
from models.common.io import InputReader
from .aunt_sue import AuntSue


def parse_aunt_sue_collection(input_reader: InputReader) -> Iterator[AuntSue]:
    for line in input_reader.readlines():
        parts = line.split(":", 1)
        sue_id = int(parts[0].replace("Sue ", ""))
        attributes = {}
        for attribute in parts[1].split(","):
            key, value = attribute.split(":")
            attributes[key.strip()] = int(value.strip())
        yield AuntSue(sue_id, attributes)
