from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .sequence_generator import SequenceGenerator, SequenceMatchFinder


def aoc_2017_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 15, "Dueling Generators")
    io_handler.output_writer.write_header(problem_id)
    start_a, start_b = [
        int(line.split()[-1]) for line in io_handler.input_reader.readlines()
    ]
    divisor = 2_147_483_647
    generator_a = SequenceGenerator(start_a, factor=16_807, divisor=divisor)
    generator_b = SequenceGenerator(start_b, factor=48_271, divisor=divisor)
    match_finder = SequenceMatchFinder(generator_a, generator_b, num_bits_to_match=16)
    num_matches = match_finder.num_matches(
        num_steps=40_000_000, progress_bar=io_handler.progress_bar
    )
    yield ProblemSolution(
        problem_id,
        f"Number of matches not filtering out multiples: {num_matches}",
        part=1,
        result=num_matches,
    )

    generator_a.filter_multiples_of = 4
    generator_b.filter_multiples_of = 8
    num_matches = match_finder.num_matches(
        num_steps=5_000_000, progress_bar=io_handler.progress_bar
    )
    yield ProblemSolution(
        problem_id,
        f"Number of matches filtering out multiples: {num_matches}",
        part=2,
        result=num_matches,
    )
