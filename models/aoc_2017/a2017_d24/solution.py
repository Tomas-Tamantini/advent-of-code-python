from models.common.io import IOHandler
from .parser import parse_bridge_components
from .bridge_builder import BridgeBuilder


def aoc_2017_d24(io_handler: IOHandler) -> None:
    print("--- AOC 2017 - Day 24: Electromagnetic Moat ---")
    components = list(parse_bridge_components(io_handler.input_reader))
    builder = BridgeBuilder(components)
    print("Be patient, it takes ~1min to run", end="\r")
    builder.build()
    print(f"Part 1: Maximum bridge strength: {builder.max_strength}")
    print(
        f"Part 2: Maximum strength of longest bridge: {builder.max_strength_of_longest_bridge}"
    )
