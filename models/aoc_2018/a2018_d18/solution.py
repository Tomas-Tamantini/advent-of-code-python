from models.common.io import InputReader, CharacterGrid
from .lumber_area import LumberArea, AcreType


def aoc_2018_d18(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 18: Settlers of The North Pole ---")
    grid = CharacterGrid(input_reader.read())
    area = LumberArea(width=grid.width, height=grid.height)
    cells = grid.tiles
    cells_after_10 = area.multi_step(cells, 10)
    num_wooded = sum(c == AcreType.TREE for c in cells_after_10.values())
    num_lumberyards = sum(c == AcreType.LUMBERYARD for c in cells_after_10.values())
    print(f"Part 1: Resource value after 10 minutes: {num_wooded * num_lumberyards}")
    print("Part 2 - Be patient, it takes about a minute to run", end="\r")
    cells_after_1b = area.multi_step(cells, 1_000_000_000)
    num_wooded = sum(c == AcreType.TREE for c in cells_after_1b.values())
    num_lumberyards = sum(c == AcreType.LUMBERYARD for c in cells_after_1b.values())
    print(
        f"Part 2: Resource value after 1 billion minutes: {num_wooded * num_lumberyards}"
    )
