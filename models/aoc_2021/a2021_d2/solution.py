from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_submarine_navigation_instructions
from .submarine import Submarine


def aoc_2021_d2(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 2, "Dive!")
    io_handler.output_writer.write_header(problem_id)
    submarine = Submarine()
    instructions_without_aim = list(
        parse_submarine_navigation_instructions(
            io_handler.input_reader, submarine_has_aim=False
        )
    )
    for instruction in instructions_without_aim:
        submarine = instruction.execute(submarine)
    product = submarine.position.x * submarine.position.y
    solution = ProblemSolution(
        problem_id,
        f"The product of the final position without aim is {product}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)

    submarine = Submarine()
    instructions_with_aim = list(
        parse_submarine_navigation_instructions(
            io_handler.input_reader, submarine_has_aim=True
        )
    )
    for instruction in instructions_with_aim:
        submarine = instruction.execute(submarine)

    product = submarine.position.x * submarine.position.y
    solution = ProblemSolution(
        problem_id, f"The product of the final position with aim is {product}", part=2
    )
    io_handler.output_writer.write_solution(solution)
