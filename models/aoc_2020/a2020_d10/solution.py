from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .adapter_array import AdapterArray


def aoc_2020_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 10, "Adapter Array")
    io_handler.output_writer.write_header(problem_id)
    adapters = [int(line) for line in io_handler.input_reader.readlines()]
    array = AdapterArray(
        outlet_joltage=0,
        device_joltage=max(adapters) + 3,
        max_joltage_difference=3,
        adapter_ratings=adapters,
    )
    differences = array.joltage_differences_of_sorted_adapters()
    num_1_diff = differences.count(1)
    num_3_diff = differences.count(3)
    result = num_1_diff * num_3_diff
    yield ProblemSolution(problem_id, f"{result} joltage differences", result, part=1)

    num_arrangements = array.number_of_arrangements()
    yield ProblemSolution(
        problem_id, f"{num_arrangements} arrangements", part=2, result=num_arrangements
    )
