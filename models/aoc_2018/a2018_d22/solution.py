from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .rocky_cave import RockyCave, CaveExplorer


def aoc_2018_d22(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2018 - Day 22: Mode Maze ---")
    lines = list(io_handler.input_reader.readlines())
    depth = int(lines[0].split()[1])
    target = Vector2D(*map(int, lines[1].split()[1].split(",")))
    cave = RockyCave(
        depth=depth,
        target=target,
        row_multiplier=16807,
        col_multiplier=48271,
        erosion_level_mod=20183,
    )
    risk_level = cave.risk_level()
    print(f"Part 1: Risk level of cave: {risk_level}")
    explorer = CaveExplorer(cave, time_to_move=1, time_to_switch_gear=7)
    shortest_time = explorer.shortest_time_to_target()
    print(f"Part 2: Shortest time to reach target: {shortest_time}")
