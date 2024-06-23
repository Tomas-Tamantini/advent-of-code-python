from models.common.io import IOHandler, CharacterGrid
from .smoke_basin import SmokeBasin


def aoc_2021_d9(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2021 - Day 9: Smoke Basin ---")
    grid = CharacterGrid(io_handler.input_reader.read())
    basin = SmokeBasin(
        heightmap={pos: int(height) for pos, height in grid.tiles.items()}
    )
    risk_level = sum(height + 1 for _, height in basin.local_minima())
    print(f"Part 1: The risk value of the smoke basin is {risk_level}")

    area_sizes = [len(area) for area in basin.areas()]
    three_largest_areas = sorted(area_sizes, reverse=True)[:3]
    product = three_largest_areas[0] * three_largest_areas[1] * three_largest_areas[2]
    print(f"Part 2: The product of the three largest areas is {product}")
