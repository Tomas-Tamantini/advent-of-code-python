from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .cylindrical_forest import CylindricalForest


def aoc_2020_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 3, "Toboggan Trajectory")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    forest = CylindricalForest(
        width=grid.width, height=grid.height, trees=set(grid.positions_with_value("#"))
    )
    num_collisions = forest.number_of_collisions_with_trees(steps_right=3, steps_down=1)
    yield ProblemSolution(
        problem_id,
        f"{num_collisions} collisions with trees",
        part=1,
        result=num_collisions,
    )

    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = 1
    for steps_right, steps_down in slopes:
        num_collisions = forest.number_of_collisions_with_trees(
            steps_right=steps_right, steps_down=steps_down
        )
        product *= num_collisions
    yield ProblemSolution(
        problem_id, f"Product of collisions: {product}", part=2, result=product
    )
