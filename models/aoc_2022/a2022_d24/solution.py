from models.common.io import IOHandler
from .parser import parse_blizzard_valley
from .logic import BlizzardMazeSolver


def aoc_2022_d24(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2022, 24, "Blizzard Basin")
    valley = parse_blizzard_valley(io_handler.input_reader)
    solver = BlizzardMazeSolver(valley)
    print("Part 1: Be patient, it takes about 20s to run", end="\r")
    min_steps = solver.min_steps_to_exit()
    print(f"Part 1: The minimum number of steps to exit valley is {min_steps}")
    print("Part 2: Be patient, it takes about 1min to run", end="\r")
    min_steps = solver.min_steps_to_exit(num_returns_to_start=1)
    print(f"Part 2: The minimum number of steps to exit valley twice is {min_steps}")
