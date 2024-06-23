from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .asteroid_belt import AsteroidBelt


def aoc_2019_d10(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 10, "Monitoring Station")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    belt = AsteroidBelt(asteroids=set(grid.positions_with_value("#")))
    most_visible, others_visible = belt.asteroid_with_most_visibility()
    solution = ProblemSolution(
        problem_id, f"Best location can see {others_visible} other asteroids", part=1
    )
    io_handler.output_writer.write_solution(solution)
    vaporized = list(belt.vaporize_asteroids_from(most_visible))
    two_hundredth = vaporized[199]
    product = two_hundredth.x * 100 + two_hundredth.y
    solution = ProblemSolution(
        problem_id, f"200th asteroid to be vaporized is at {two_hundredth.x}, {two_hundredth.y} - product: {product}", part=2
    )
    io_handler.output_writer.write_solution(solution)
