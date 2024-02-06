from models.vectors import Vector2D, BoundingBox
from models.aoc_2018.a2018_d22 import RockyCave


def test_rocky_cave_erosion_levels_are_calculated_properly():
    cave = RockyCave(
        depth=510,
        target=Vector2D(10, 10),
        row_multiplier=16807,
        col_multiplier=48271,
        erosion_level_mod=20183,
    )
    assert cave.erosion_level(Vector2D(0, 0)) == 510
    assert cave.erosion_level(Vector2D(1, 0)) == 17317
    assert cave.erosion_level(Vector2D(0, 1)) == 8415
    assert cave.erosion_level(Vector2D(1, 1)) == 1805
    assert cave.erosion_level(Vector2D(10, 10)) == 510


def test_risk_level_is_calculated_properly():
    cave = RockyCave(
        depth=510,
        target=Vector2D(10, 10),
        row_multiplier=16807,
        col_multiplier=48271,
        erosion_level_mod=20183,
    )
    region = BoundingBox(
        bottom_left=Vector2D(0, 0),
        top_right=Vector2D(10, 10),
    )
    assert cave.risk_level(region) == 114