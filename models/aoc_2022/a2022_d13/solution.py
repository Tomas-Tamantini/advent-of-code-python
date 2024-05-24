from models.common.io import InputReader
from .packet_comparison import left_packet_leq_right


def aoc_2022_d13(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 13: Distress Signal ---")
    lines = list(input_reader.read_stripped_lines())
    sum_pair_indices = 0
    for pair_index in range(len(lines) // 2):
        packet_left = eval(lines[2 * pair_index])
        packet_right = eval(lines[2 * pair_index + 1])
        if left_packet_leq_right(packet_left, packet_right):
            sum_pair_indices += pair_index + 1
    print(f"Part 1: Sum of pair indices is {sum_pair_indices}")
