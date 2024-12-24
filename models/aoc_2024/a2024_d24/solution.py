from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import (
    Circuit,
    PulseType,
    swapped_pair_of_wires_for_full_adder,
)
from .parser import parse_input_pulses, parse_logic_gates

# TODO: Try to merge pulse and circuit logic with AOC 2023 - Day 20


def aoc_2024_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 24, "Crossed Wires")
    io_handler.output_writer.write_header(problem_id)
    gates = list(parse_logic_gates(io_handler.input_reader))
    input_pulses = list(parse_input_pulses(io_handler.input_reader))
    circuit = Circuit(gates)

    output_sum = 0
    for output_pulse in circuit.propagate(input_pulses):
        if (
            output_pulse.wire.startswith("z")
            and output_pulse.pulse_type == PulseType.HIGH
        ):
            output_sum += 2 ** int(output_pulse.wire[1:])

    yield ProblemSolution(
        problem_id, f"The output value is {output_sum}", result=output_sum, part=1
    )

    swapped = set()
    for pair in swapped_pair_of_wires_for_full_adder(gates):
        swapped.update(pair)

    result = ",".join(sorted(swapped))
    yield ProblemSolution(problem_id, f"The swapped wires are {result}", result, part=2)
