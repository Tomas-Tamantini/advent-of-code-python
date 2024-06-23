from models.common.io import IOHandler
from .parser import parse_submarine_navigation_instructions
from .submarine import Submarine


def aoc_2021_d2(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2021 - Day 2: Dive! ---")
    submarine = Submarine()
    instructions_without_aim = list(
        parse_submarine_navigation_instructions(
            io_handler.input_reader, submarine_has_aim=False
        )
    )
    for instruction in instructions_without_aim:
        submarine = instruction.execute(submarine)
    product = submarine.position.x * submarine.position.y
    print(f"Part 1: The product of the final position without aim is {product}")

    submarine = Submarine()
    instructions_with_aim = list(
        parse_submarine_navigation_instructions(
            io_handler.input_reader, submarine_has_aim=True
        )
    )
    for instruction in instructions_with_aim:
        submarine = instruction.execute(submarine)

    product = submarine.position.x * submarine.position.y
    print(f"Part 2: The product of the final position with aim is {product}")
