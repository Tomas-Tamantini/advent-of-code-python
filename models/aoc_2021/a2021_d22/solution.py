from models.common.io import InputReader
from .parser import parse_cuboid_instructions
from .reactor_cells import num_reactor_cells_on


def aoc_2021_d22(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 22: Reactor Reboot ---")
    instructions = list(parse_cuboid_instructions(input_reader))
    small_instructions = [
        instruction
        for instruction in instructions
        if instruction.cuboid.all_coords_are_between(-50, 50)
    ]
    print(
        f"Part 1: The number of cells turned on in smaller volume is {num_reactor_cells_on(small_instructions)}"
    )
    print(
        f"Part 2: The number of cells turned on in entire volume is {num_reactor_cells_on(instructions)}"
    )
