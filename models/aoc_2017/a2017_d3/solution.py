from models.common.io import IOHandler, Problem, ProblemSolution
from .square_spiral import SquareSpiral


def aoc_2017_d3(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 3, "Spiral Memory")
    io_handler.output_writer.write_header(problem_id)
    target = int(io_handler.input_reader.read().strip())
    target_coordinates = SquareSpiral.coordinates(target)
    manhattan_distance = target_coordinates.manhattan_size
    solution = ProblemSolution(
        problem_id, f"Manhattan distance to {target}: {manhattan_distance}", part=1
    )
    io_handler.set_solution(solution)
    first_value_larger_than_input = -1
    for value in SquareSpiral.adjacent_sum_sequence():
        if value > target:
            first_value_larger_than_input = value
            break
    solution = ProblemSolution(
        problem_id,
        f"First sequence term larger than {target}: {first_value_larger_than_input}",
        part=2,
    )
    io_handler.set_solution(solution)
