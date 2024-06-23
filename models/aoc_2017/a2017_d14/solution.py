from models.common.io import IOHandler
from .disk_grid import DiskGrid


def aoc_2017_d14(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2017 - Day 14: Disk Defragmentation ---")
    key = io_handler.input_reader.read().strip()
    num_rows = 128
    grid = DiskGrid(key, num_rows)
    print(f"Part 1: Number of used squares: {grid.num_used_squares()}")
    print(f"Part 2: Number of regions: {grid.num_regions()}")
