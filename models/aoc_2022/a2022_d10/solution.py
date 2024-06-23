from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_instructions_with_duration
from .logic import RegisterHistory, SpriteScreen


def aoc_2022_d10(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 10, "Cathode-Ray Tube")
    io_handler.output_writer.write_header(problem_id)
    rh = RegisterHistory()
    for instruction in parse_instructions_with_duration(io_handler.input_reader):
        rh.run_instruction(instruction)
    strengths = [cycle * rh.value_during_cycle(cycle) for cycle in range(20, 221, 40)]
    solution = ProblemSolution(
        problem_id,
        f"Sum of strengths at cycles 20, 60, 100, 140, and 180: {sum(strengths)}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    screen = SpriteScreen(width=40, height=6, sprite_length=3)
    sprite_center_positions = rh.register_values
    solution = ProblemSolution(
        problem_id,
        f"The message formed by the sprite is\n\n{screen.draw(sprite_center_positions)}\n",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
