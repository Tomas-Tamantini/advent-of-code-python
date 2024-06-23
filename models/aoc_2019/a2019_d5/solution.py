from models.common.io import IOHandler, Problem
from .air_conditioner import run_air_conditioner_program


def aoc_2019_d5(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 5, "Sunny with a Chance of Asteroids")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    output_1 = run_air_conditioner_program(instructions, air_conditioner_id=1)
    print(f"Part 1: Diagnostic code for air conditioner 1 is {output_1}")
    output_5 = run_air_conditioner_program(instructions, air_conditioner_id=5)
    print(f"Part 2: Diagnostic code for air conditioner 5 is {output_5}")
