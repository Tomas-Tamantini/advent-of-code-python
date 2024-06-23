from models.common.io import IOHandler, CharacterGrid
from models.common.vectors import VectorNDimensional
from .hyper_game_of_life import HyperGameOfLife


def aoc_2020_d17(io_handler: IOHandler) -> None:
    print("--- AOC 2020 - Day 17: Conway Cubes ---")
    grid = CharacterGrid(io_handler.input_reader.read())
    active_cubes_3d = {
        VectorNDimensional(pos.x, pos.y, 0) for pos in grid.positions_with_value("#")
    }
    automaton = HyperGameOfLife()
    for _ in range(6):
        active_cubes_3d = automaton.next_state(active_cubes_3d)
    print(f"Part 1: Number of active 3D cubes is {len(active_cubes_3d)}")

    active_cubes_4d = {
        VectorNDimensional(pos.x, pos.y, 0, 0) for pos in grid.positions_with_value("#")
    }
    automaton = HyperGameOfLife()
    for _ in range(6):
        active_cubes_4d = automaton.next_state(active_cubes_4d)
    print(f"Part 2: Number of active 4D hypercubes is {len(active_cubes_4d)}")
