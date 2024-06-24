from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .frequency_transmission import flawed_frequency_transmission


def aoc_2019_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 16, "Flawed Frequency Transmission")
    io_handler.output_writer.write_header(problem_id)
    signal = list(map(int, io_handler.input_reader.read().strip()))

    output = flawed_frequency_transmission(
        signal, num_phases=100, num_elements_result=8
    )
    digits = "".join(map(str, output))
    yield ProblemSolution(
        problem_id, f"First 8 digits after 100 phases are {digits}", part=1
    )

    signal = signal * 10_000
    offset = int("".join(map(str, signal[:7])))
    output = flawed_frequency_transmission(
        signal, num_phases=100, offset=offset, num_elements_result=8
    )
    digits = "".join(map(str, output))
    yield ProblemSolution(
        problem_id, f"8 digits of larger signal after 100 phases are {digits}", part=2
    )
