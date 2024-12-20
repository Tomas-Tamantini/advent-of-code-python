from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .josephus import josephus, modified_josephus


def aoc_2016_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 19, "An Elephant Named Joseph")
    io_handler.output_writer.write_header(problem_id)
    num_elves = int(io_handler.input_reader.read().strip())
    winning_elf_take_left = josephus(num_elves)
    yield ProblemSolution(
        problem_id,
        f"Winning elf if they take from the left: {winning_elf_take_left}",
        part=1,
        result=winning_elf_take_left,
    )

    winning_elf_take_across = modified_josephus(num_elves)
    yield ProblemSolution(
        problem_id,
        f"Winning elf if they take from across: {winning_elf_take_across}",
        part=2,
        result=winning_elf_take_across,
    )
