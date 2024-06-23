from models.common.io import IOHandler, Problem, ProblemSolution
from models.aoc_2019.a2019_d5.air_conditioner import run_air_conditioner_program


def aoc_2019_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 9, "Sensor Boost")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    output = run_air_conditioner_program(instructions, air_conditioner_id=1)
    solution = ProblemSolution(
        problem_id, f"Output for the BOOST program is {output}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    output = run_air_conditioner_program(instructions, air_conditioner_id=2)
    solution = ProblemSolution(
        problem_id, f"Coordinates of the distress signal are {output}", part=2
    )
    io_handler.output_writer.write_solution(solution)
