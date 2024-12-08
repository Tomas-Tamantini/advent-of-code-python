from itertools import permutations
from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .amplifiers import Amplifiers


def aoc_2019_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 7, "Amplification Circuit")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    amplifiers = Amplifiers(instructions)
    input_signal = 0
    max_signal = max(
        amplifiers.run(phase_settings, input_signal)
        for phase_settings in permutations(range(5))
    )
    yield ProblemSolution(
        problem_id,
        f"Maximum signal that can be sent to the thrusters is {max_signal}",
        part=1,
        result=max_signal,
    )

    max_signal_feedback = max(
        amplifiers.run_with_feedback(phase_settings, input_signal)
        for phase_settings in permutations(range(5, 10))
    )
    yield ProblemSolution(
        problem_id,
        (
            f"Maximum signal that can be sent to the"
            f" thrusters with feedback is {max_signal_feedback}"
        ),
        part=2,
        result=max_signal_feedback,
    )
