from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .asteroid_belt import AsteroidBelt


def aoc_2019_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 10, "Monitoring Station")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    belt = AsteroidBelt(asteroids=set(grid.positions_with_value("#")))
    most_visible, others_visible = belt.asteroid_with_most_visibility()
    yield ProblemSolution(
        problem_id,
        f"Best location can see {others_visible} other asteroids",
        part=1,
        result=others_visible,
    )

    vaporized = list(belt.vaporize_asteroids_from(most_visible))
    two_hundredth = vaporized[199]
    result = two_hundredth.x * 100 + two_hundredth.y
    yield ProblemSolution(
        problem_id,
        (
            "200th asteroid to be vaporized is at "
            f"{two_hundredth.x}, {two_hundredth.y} - product: {result}"
        ),
        result,
        part=2,
    )
