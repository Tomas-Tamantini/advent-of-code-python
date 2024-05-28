from models.common.io import InputReader
from .frequency_transmission import flawed_frequency_transmission


def aoc_2019_d16(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 16: Flawed Frequency Transmission ---")
    signal = list(map(int, input_reader.read().strip()))

    output = flawed_frequency_transmission(
        signal, num_phases=100, num_elements_result=8
    )
    digits = "".join(map(str, output))
    print(f"Part 1: First 8 digits after 100 phases are {digits}")
    signal = signal * 10_000
    offset = int("".join(map(str, signal[:7])))
    output = flawed_frequency_transmission(
        signal, num_phases=100, offset=offset, num_elements_result=8
    )
    digits = "".join(map(str, output))
    print(f"Part 2: 8 digits of larger signal after 100 phases are {digits}")
