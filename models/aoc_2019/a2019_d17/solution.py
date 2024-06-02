from models.common.io import InputReader
from .logic import (
    ScaffoldMap,
    run_scaffolding_discovery_program,
    run_scaffolding_exploration_program,
)


def aoc_2019_d17(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 17: Set and Forget ---")
    instructions = [int(code) for code in input_reader.read().split(",")]
    scaffold_map = ScaffoldMap()
    run_scaffolding_discovery_program(scaffold_map, instructions)
    alignment_parameters = sum(
        pos.x * pos.y for pos in scaffold_map.scaffolding_intersections()
    )
    print(f"Part 1: Sum of alignment parameters is {alignment_parameters}")
    compressed_path = scaffold_map.compressed_path_through_scaffolding(
        num_subroutines=3
    )
    instructions[0] = 2
    dust_collected = run_scaffolding_exploration_program(instructions, compressed_path)
    print(f"Part 2: Dust collected by the vacuum robot is {dust_collected}")
