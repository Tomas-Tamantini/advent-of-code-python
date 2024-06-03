from collections import defaultdict
from models.common.io import InputReader
from .underwater_cave import UnderwaterCave


@staticmethod
def _parse_underwater_caves(line: str) -> tuple[UnderwaterCave, UnderwaterCave]:
    return tuple(
        UnderwaterCave(name, is_small=name.islower())
        for name in [p.strip() for p in line.split("-")]
    )


def parse_underwater_cave_connections(
    input_reader: InputReader,
) -> dict[UnderwaterCave, set[UnderwaterCave]]:
    connections = defaultdict(set)
    for line in input_reader.read_stripped_lines():
        cave_a, cave_b = _parse_underwater_caves(line)
        connections[cave_a].add(cave_b)

    return connections
