from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .message_reconstructor import MessageReconstructor


def aoc_2016_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 6, "Signals and Noise")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    message_reconstructor = MessageReconstructor(lines)
    most_common_chars = (
        message_reconstructor.reconstruct_message_from_most_common_chars()
    )
    yield ProblemSolution(
        problem_id,
        f"Message reconstructed from most common letters: {most_common_chars}",
        part=1,
        result=most_common_chars,
    )

    least_common_chars = (
        message_reconstructor.reconstruct_message_from_least_common_chars()
    )
    yield ProblemSolution(
        problem_id,
        f"Message reconstructed from least common letters: {least_common_chars}",
        part=2,
        result=least_common_chars,
    )
