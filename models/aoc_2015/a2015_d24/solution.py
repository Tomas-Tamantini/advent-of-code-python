from models.common.io import IOHandler
from math import prod
from .packet_arrangement import possible_arrangements_of_packets_in_passenger_comparment


def aoc_2015_d24(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 24: It Hangs in the Balance ---")
    lines = list(io_handler.input_reader.readlines())
    numbers = tuple(int(l) for l in lines)
    min_quantum_entanglement = min(
        prod(group)
        for group in possible_arrangements_of_packets_in_passenger_comparment(
            numbers, num_groups=3
        )
    )
    print(
        f"Part 1: Quantum entanglement of optimal arrangement divided in 3 groups is {min_quantum_entanglement}"
    )
    min_quantum_entanglement = min(
        prod(group)
        for group in possible_arrangements_of_packets_in_passenger_comparment(
            numbers, num_groups=4
        )
    )
    print(
        f"Part 2: Quantum entanglement of optimal arrangement divided in 4 groups is {min_quantum_entanglement}"
    )
