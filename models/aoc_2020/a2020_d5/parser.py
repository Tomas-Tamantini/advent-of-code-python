from typing import Iterator

from models.common.io import InputReader


def parse_plane_seat_ids(input_reader: InputReader) -> Iterator[int]:
    for line in input_reader.readlines():
        line = line.strip()
        if line:
            row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
            col = int(line[7:].replace("L", "0").replace("R", "1"), 2)
            yield row * 8 + col
