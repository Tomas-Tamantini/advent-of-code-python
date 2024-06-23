from models.common.io import IOHandler, Problem
from .parser import parse_programmable_screen_instructions
from .programmable_screen import ProgrammableScreen


def aoc_2016_d8(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 8, "Two-Factor Authentication")
    io_handler.output_writer.write_header(problem_id)
    screen = ProgrammableScreen(width=50, height=6)
    parse_programmable_screen_instructions(io_handler.input_reader, screen)
    print(f"Part 1: Number of lit pixels: {screen.number_of_lit_pixels()}")
    print("Part 2: Screen display")
    screen_display = str(screen).replace("0", " ").replace("1", "#")
    print(screen_display)
