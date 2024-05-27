from models.common.io import InputReader, CharacterGrid
from .cylindrical_forest import CylindricalForest


def aoc_2020_d3(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 3: Toboggan Trajectory ---")
    grid = CharacterGrid(input_reader.read())
    forest = CylindricalForest(
        width=grid.width, height=grid.height, trees=set(grid.positions_with_value("#"))
    )
    num_collisions = forest.number_of_collisions_with_trees(steps_right=3, steps_down=1)
    print(f"Part 1: {num_collisions} collisions with trees")

    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = 1
    for steps_right, steps_down in slopes:
        num_collisions = forest.number_of_collisions_with_trees(
            steps_right=steps_right, steps_down=steps_down
        )
        product *= num_collisions
    print(f"Part 2: Product of collisions: {product}")
