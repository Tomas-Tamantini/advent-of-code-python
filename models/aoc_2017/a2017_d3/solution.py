from models.common.io import IOHandler, Problem
from .square_spiral import SquareSpiral


def aoc_2017_d3(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 3, "Spiral Memory")
    io_handler.output_writer.write_header(problem_id)
    target = int(io_handler.input_reader.read().strip())
    target_coordinates = SquareSpiral.coordinates(target)
    manhattan_distance = target_coordinates.manhattan_size
    print(f"Part 1: Manhattan distance to {target}: {manhattan_distance}")
    first_value_larger_than_input = -1
    for value in SquareSpiral.adjacent_sum_sequence():
        if value > target:
            first_value_larger_than_input = value
            break
    print(
        f"Part 2: First sequence term larger than {target}: {first_value_larger_than_input}"
    )
