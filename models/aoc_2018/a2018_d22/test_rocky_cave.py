from models.common.vectors import BoundingBox, Vector2D

from .rocky_cave import CaveExplorer, RockyCave


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


def test_cave_explorer_finds_shortest_time_to_target():
    cave = RockyCave(
        depth=510,
        target=Vector2D(10, 10),
        row_multiplier=16807,
        col_multiplier=48271,
        erosion_level_mod=20183,
    )
    explorer = CaveExplorer(cave, time_to_move=1, time_to_switch_gear=7)
    assert explorer.shortest_time_to_target() == 45
