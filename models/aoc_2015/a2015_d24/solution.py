from math import prod
from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .packet_arrangement import possible_arrangements_of_packets_in_passenger_comparment


def aoc_2015_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 24, "It Hangs in the Balance")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    numbers = tuple(int(l) for l in lines)
    min_quantum_entanglement = min(
        prod(group)
        for group in possible_arrangements_of_packets_in_passenger_comparment(
            numbers, num_groups=3
        )
    )
    yield ProblemSolution(
        problem_id,
        f"Quantum entanglement of optimal arrangement divided in 3 groups is {min_quantum_entanglement}",
        part=1,
        result=min_quantum_entanglement,
    )

    min_quantum_entanglement = min(
        prod(group)
        for group in possible_arrangements_of_packets_in_passenger_comparment(
            numbers, num_groups=4
        )
    )
    yield ProblemSolution(
        problem_id,
        f"Quantum entanglement of optimal arrangement divided in 4 groups is {min_quantum_entanglement}",
        result=min_quantum_entanglement,
        part=2,
    )
