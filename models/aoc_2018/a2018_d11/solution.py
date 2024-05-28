from models.common.io import InputReader, ProgressBarConsole
from .fuel_cells import FuelCells


def aoc_2018_d11(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2018 - Day 11: Chronal Charge ---")
    grid_serial_number = int(input_reader.read())
    cells = FuelCells(width=300, height=300, grid_serial_number=grid_serial_number)
    x, y = cells.position_with_largest_total_power(region_width=3, region_height=3)
    print(f"Part 1: Position with largest total power: {x+1},{y+1}")
    square = cells.square_with_largest_total_power(progress_bar)
    (x, y), s = square.coords_top_left, square.size
    print(f"Part 2: Position with largest total power and region size: {x+1},{y+1},{s}")
