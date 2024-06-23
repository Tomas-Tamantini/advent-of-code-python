from models.common.io import IOHandler, Problem
from .message_reconstructor import MessageReconstructor


def aoc_2016_d6(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 6, "Signals and Noise")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    message_reconstructor = MessageReconstructor(lines)
    most_common_chars = (
        message_reconstructor.reconstruct_message_from_most_common_chars()
    )
    print(
        f"Part 1: Message reconstructed from most common letters: {most_common_chars}"
    )
    least_common_chars = (
        message_reconstructor.reconstruct_message_from_least_common_chars()
    )
    print(
        f"Part 2: Message reconstructed from least common letters: {least_common_chars}"
    )
