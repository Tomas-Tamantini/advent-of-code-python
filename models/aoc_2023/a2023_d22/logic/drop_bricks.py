from typing import Iterator

from models.common.vectors import Vector2D

from .brick import Brick


def _distance_to_fall(brick: Brick, height: dict[Vector2D, int]) -> int:
    max_height = max(height.get(pos, 0) for pos in brick.xy_projection())
    return brick.min_z_coordinate - max_height - 1


def drop_bricks(bricks: set[Brick]) -> Iterator[Brick]:
    height = dict()
    sorted_bricks = sorted(bricks, key=lambda b: b.min_z_coordinate)
    for brick in sorted_bricks:
        distance_to_fall = _distance_to_fall(brick, height)
        dropped_brick = brick.drop(distance_to_fall)
        for pos in dropped_brick.xy_projection():
            height[pos] = dropped_brick.max_z_coordinate
        yield dropped_brick
