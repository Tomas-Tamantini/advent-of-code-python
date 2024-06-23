from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .repair_droid import DroidExploredArea, repair_droid_explore_area


def aoc_2019_d15(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 15: Oxygen System ---")
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    area = DroidExploredArea()
    repair_droid_explore_area(area, instructions)
    distance = area.distance_to_oxygen_system(starting_point=Vector2D(0, 0))
    print(
        f"Part 1: Fewest number of movement commands to reach the oxygen system is {distance}"
    )
    minutes = area.minutes_to_fill_with_oxygen()
    print(f"Part 2: Minutes to fill the area with oxygen is {minutes}")
