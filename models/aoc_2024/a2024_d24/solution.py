from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import Circuit, PulseType
from .parser import parse_input_pulses, parse_logic_gates

# TODO: Try to merge pulse and circuit logic with AOC 2023 - Day 20


def aoc_2024_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 24, "Crossed Wires")
    io_handler.output_writer.write_header(problem_id)
    gates = list(parse_logic_gates(io_handler.input_reader))
    input_pulses = list(parse_input_pulses(io_handler.input_reader))
    circuit = Circuit(gates)

    output_pulses = dict()
    for output_pulse in circuit.propagate(input_pulses):
        output_pulses[output_pulse.wire] = output_pulse.pulse_type
    out_gates = sorted(wire for wire in output_pulses if wire.startswith("z"))
    out_value = sum(
        2**i
        for i, wire in enumerate(out_gates)
        if output_pulses[wire] == PulseType.HIGH
    )
    yield ProblemSolution(
        problem_id, f"The output value is {out_value}", result=out_value, part=1
    )
