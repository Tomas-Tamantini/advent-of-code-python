from models.common.vectors import Vector2D

from ..logic import CollinearAntinodeGenerator, TwiceDistanceAntinodeGenerator


def test_twice_distance_antinode_generator_yields_with_distances_in_proportion_2_to_1():
    generator = TwiceDistanceAntinodeGenerator()
    antinodes = set(
        generator.antinodes(Vector2D(0, 0), Vector2D(12, 15), lambda _: True)
    )
    assert antinodes == {
        Vector2D(24, 30),
        Vector2D(4, 5),
        Vector2D(8, 10),
        Vector2D(-12, -15),
    }


def test_twice_distance_antinode_generator_check_if_nodes_are_within_bounds():
    generator = TwiceDistanceAntinodeGenerator()
    antinodes = set(
        generator.antinodes(
            Vector2D(0, 0),
            Vector2D(12, 15),
            is_within_bounds=lambda v: v.x == -12,
        )
    )
    assert antinodes == {
        Vector2D(-12, -15),
    }


def test_collinear_antinode_generator_yields_all_collinear_points_within_bounds():
    def is_within_bounds(pos: Vector2D) -> bool:
        return 0 <= pos.x <= 13 and 0 <= pos.y <= 13

    generator = CollinearAntinodeGenerator()
    antinodes = set(
        generator.antinodes(Vector2D(3, 4), Vector2D(7, 10), is_within_bounds)
    )
    assert antinodes == {
        Vector2D(x=1, y=1),
        Vector2D(x=3, y=4),
        Vector2D(x=5, y=7),
        Vector2D(x=7, y=10),
        Vector2D(x=9, y=13),
    }
