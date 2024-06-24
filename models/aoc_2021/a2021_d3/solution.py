from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .bit_frequency import BitFrequency


def aoc_2021_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 3, "Binary Diagnostic")
    io_handler.output_writer.write_header(problem_id)
    binary_strings = [line.strip() for line in io_handler.input_reader.readlines()]
    frequency = BitFrequency(binary_strings)
    most_frequent = frequency.most_frequent_bits_in_each_position()
    least_frequent = frequency.least_frequent_bits_in_each_position()
    product = int(most_frequent, 2) * int(least_frequent, 2)
    yield ProblemSolution(
        problem_id,
        f"The product of the most and least frequent bits is {product}",
        part=1,
    )

    filtered_most_frequent = frequency.filter_down_to_one(filter_by_most_common=True)
    filtered_least_frequent = frequency.filter_down_to_one(filter_by_most_common=False)
    product = int(filtered_most_frequent, 2) * int(filtered_least_frequent, 2)
    yield ProblemSolution(
        problem_id,
        f"The product of the most and least frequent bits in filtered strings is {product}",
        part=2,
    )
