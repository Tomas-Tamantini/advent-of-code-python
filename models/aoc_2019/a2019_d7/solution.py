from itertools import permutations
from models.common.io import IOHandler, Problem
from .amplifiers import Amplifiers


def aoc_2019_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 7, "Amplification Circuit")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    amplifiers = Amplifiers(instructions)
    input_signal = 0
    max_signal = max(
        amplifiers.run(phase_settings, input_signal)
        for phase_settings in permutations(range(5))
    )
    print(f"Part 1: Maximum signal that can be sent to the thrusters is {max_signal}")
    max_signal_feedback = max(
        amplifiers.run_with_feedback(phase_settings, input_signal)
        for phase_settings in permutations(range(5, 10))
    )
    print(
        f"Part 2: Maximum signal that can be sent to the thrusters with feedback is {max_signal_feedback}"
    )
