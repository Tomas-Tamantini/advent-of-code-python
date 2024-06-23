from models.common.io import IOHandler, CharacterGrid
from .asteroid_belt import AsteroidBelt


def aoc_2019_d10(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2019, 10, "Monitoring Station")
    grid = CharacterGrid(io_handler.input_reader.read())
    belt = AsteroidBelt(asteroids=set(grid.positions_with_value("#")))
    most_visible, others_visible = belt.asteroid_with_most_visibility()
    print(f"Part 1: Best location can see {others_visible} other asteroids")
    vaporized = list(belt.vaporize_asteroids_from(most_visible))
    two_hundredth = vaporized[199]
    product = two_hundredth.x * 100 + two_hundredth.y
    print(
        f"Part 2: 200th asteroid to be vaporized is at {two_hundredth.x}, {two_hundredth.y} - product: {product}"
    )
