from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_layered_firewall


def aoc_2017_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 13, "Packet Scanners")
    io_handler.output_writer.write_header(problem_id)
    firewall = parse_layered_firewall(io_handler.input_reader)
    packet_collisions = list(firewall.packet_collisions())
    severity = sum(
        layer_depth * layer.scanning_range for layer_depth, layer in packet_collisions
    )
    yield ProblemSolution(
        problem_id,
        f"Severity of packet collisions: {severity}",
        part=1,
        result=severity,
    )

    minimum_delay = firewall.minimum_delay_to_avoid_collisions()
    yield ProblemSolution(
        problem_id,
        f"Minimum delay to avoid collisions: {minimum_delay}",
        part=2,
        result=minimum_delay,
    )
