from models.common.io import IOHandler
from .beam_area import BeamArea, run_beam_scanner, square_closest_to_beam_source


def aoc_2019_d19(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 19: Tractor Beam ---")
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    area = BeamArea(width=50, height=50)
    run_beam_scanner(instructions, area)
    print(
        f"Part 1: Number of points attracted to the beam is {area.num_points_attracted_to_beam}"
    )
    square_position = square_closest_to_beam_source(
        side_length=100, instructions=instructions, scanned_area=area
    )
    answer = square_position.x * 10_000 + square_position.y
    print(f"Part 2: Position of the square closest to the beam source is at {answer}")
