from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector3D
from .underwater_scanner import UnderwaterScanner


def parse_underwater_scanners(input_reader: InputReader) -> Iterator[UnderwaterScanner]:
    current_positions = []
    current_scanner_id = -1
    for line in input_reader.read_stripped_lines():
        if "scanner" in line:
            if current_positions:
                yield UnderwaterScanner(current_scanner_id, tuple(current_positions))
            current_scanner_id = int(line.split()[2])
            current_positions = []
        else:
            current_positions.append(Vector3D(*map(int, line.split(","))))
    if current_positions:
        yield UnderwaterScanner(current_scanner_id, tuple(current_positions))
