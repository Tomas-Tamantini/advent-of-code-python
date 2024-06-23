from models.common.io import IOHandler
from .parser import parse_and_give_light_grid_instructions
from .light_grid import LightGrid


def aoc_2015_d6(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 6: Probably a Fire Hazard ---")
    grid = LightGrid(1000, 1000)
    parse_and_give_light_grid_instructions(io_handler.input_reader, grid)
    print(f"Part 1: There are {grid.num_lights_on} lights on")
    grid = LightGrid(1000, 1000)
    parse_and_give_light_grid_instructions(
        io_handler.input_reader, grid, use_elvish_tongue=True
    )
    print(f"Part 2: The total brightness is {grid.num_lights_on}")
