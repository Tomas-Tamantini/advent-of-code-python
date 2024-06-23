from typing import Iterator
from models.common.io import IOHandler


def eggnog_partition(total_volume: int, capacities: list[int]) -> Iterator[list[int]]:
    if total_volume == 0:
        yield []
    elif len(capacities) > 0:
        for partition in eggnog_partition(total_volume, capacities[1:]):
            yield partition
        if total_volume >= capacities[0]:
            for partition in eggnog_partition(
                total_volume - capacities[0], capacities[1:]
            ):
                yield [capacities[0]] + partition


def aoc_2015_d17(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 17: No Such Thing as Too Much ---")
    lines = list(io_handler.input_reader.readlines())
    capacities = [int(l) for l in lines]
    total_volume = 150
    partitions = list(eggnog_partition(total_volume, capacities))
    num_ways = len(partitions)
    print(f"Part 1: There are {num_ways} ways to store eggnog")
    min_num_containers = min(len(p) for p in partitions)
    num_ways_min_containers = sum(1 for p in partitions if len(p) == min_num_containers)
    print(
        f"Part 2: There are {num_ways_min_containers} ways to store eggnog using {min_num_containers} containers"
    )
