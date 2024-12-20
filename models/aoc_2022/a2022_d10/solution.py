from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import RegisterHistory, SpriteScreen
from .parser import parse_instructions_with_duration


def aoc_2022_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 10, "Cathode-Ray Tube")
    io_handler.output_writer.write_header(problem_id)
    rh = RegisterHistory()
    for instruction in parse_instructions_with_duration(io_handler.input_reader):
        rh.run_instruction(instruction)
    strengths = [cycle * rh.value_during_cycle(cycle) for cycle in range(20, 221, 40)]
    result = sum(strengths)
    yield ProblemSolution(
        problem_id,
        f"Sum of strengths at cycles 20, 60, 100, 140, and 180: {result}",
        result,
        part=1,
    )

    screen = SpriteScreen(width=40, height=6, sprite_length=3)
    sprite_center_positions = rh.register_values
    result = screen.draw(sprite_center_positions)
    yield ProblemSolution(
        problem_id, f"The message formed by the sprite is\n\n{result}\n", result, part=2
    )
