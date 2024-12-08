from models.common.vectors import Vector2D

from ..logic import TwiceDistanceAntinodeGenerator


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
