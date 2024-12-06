from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_programmable_screen_instructions
from .programmable_screen import ProgrammableScreen


def aoc_2016_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 8, "Two-Factor Authentication")
    io_handler.output_writer.write_header(problem_id)
    screen = ProgrammableScreen(width=50, height=6)
    parse_programmable_screen_instructions(io_handler.input_reader, screen)
    result = screen.number_of_lit_pixels()
    yield ProblemSolution(problem_id, f"Number of lit pixels: {result}", result, part=1)

    screen_display = str(screen).replace("0", " ").replace("1", "#")
    yield ProblemSolution(
        problem_id,
        f"Screen display\n\n{screen_display}\n",
        part=2,
        result=screen_display,
    )
