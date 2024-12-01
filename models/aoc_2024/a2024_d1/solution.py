from typing import Iterator
from collections import defaultdict
from models.common.io import IOHandler, Problem, ProblemSolution, InputReader


def _parse_elements(input_reader: InputReader) -> Iterator[tuple[int, int]]:
    for line in input_reader.read_stripped_lines():
        yield tuple(map(int, line.split()))


def _parse_lists(input_reader: InputReader) -> tuple[list[int], list[int]]:
    first_list, second_list = [], []
    for first, second in _parse_elements(input_reader):
        first_list.append(first)
        second_list.append(second)
    return first_list, second_list


def aoc_2024_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 1, "Historian Hysteria")
    io_handler.output_writer.write_header(problem_id)
    first_list, second_list = _parse_lists(io_handler.input_reader)

    sorted_first = sorted(first_list)
    sorted_second = sorted(second_list)
    diff = sum(abs(a - b) for a, b in zip(sorted_first, sorted_second))

    yield ProblemSolution(
        problem_id, f"The distance between the two lists is {diff}", result=diff, part=1
    )

    frequency = defaultdict(int)
    for number in second_list:
        frequency[number] += 1

    similarity_score = sum(n * frequency[n] for n in first_list)
    yield ProblemSolution(
        problem_id,
        f"The similarity score between the two lists is {similarity_score}",
        result=similarity_score,
        part=2,
    )
