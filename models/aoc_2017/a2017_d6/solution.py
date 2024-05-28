from models.common.io import InputReader
from .memory_bank import MemoryBankBalancer


def aoc_2017_d6(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 6: Memory Reallocation ---")
    num_blocks = [int(block) for block in input_reader.read().split()]
    balancer = MemoryBankBalancer(num_blocks)
    num_redistributions = len(list(balancer.unique_configurations()))
    print(f"Part 1: Number of redistributions: {num_redistributions}")
    loop_size = balancer.loop_size()
    print(f"Part 2: Loop size: {loop_size}")
