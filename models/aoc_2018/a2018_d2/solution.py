from typing import Iterator
from itertools import combinations
from models.common.io import IOHandler, Problem, ProblemSolution


def contains_exactly_n_of_any_letter(string: str, n: int) -> bool:
    return any(string.count(letter) == n for letter in string)


def differing_indices(string_a: str, string_b: str) -> Iterator[int]:
    for index, (a, b) in enumerate(zip(string_a, string_b)):
        if a != b:
            yield index


def aoc_2018_d2(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 2, "Inventory Management System")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    ids = [line.strip() for line in lines]
    exactly_two = sum(contains_exactly_n_of_any_letter(id, 2) for id in ids)
    exactly_three = sum(contains_exactly_n_of_any_letter(id, 3) for id in ids)
    solution = ProblemSolution(
        problem_id, f"Checksum of ids is {exactly_two * exactly_three}", part=1
    )
    io_handler.set_solution(solution)
    letters_in_common = ""
    for i, j in combinations(range(len(ids)), 2):
        differing = list(differing_indices(ids[i], ids[j]))
        if len(differing) == 1:
            letters_in_common = ids[i][: differing[0]] + ids[i][differing[0] + 1 :]
            break

    solution = ProblemSolution(
        problem_id, f"Letters in common between ids are {letters_in_common}", part=2
    )
    io_handler.set_solution(solution)
