import pytest
from models.common.vectors import Vector2D, CardinalDirection
from .tree_height_map import TreeHeightMap


def test_tree_height_map_iterates_through_trees_visible_from_given_direction():
    tree_height_map = TreeHeightMap(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )
    visible_north = list(
        tree_height_map.visible_trees(looking_direction=CardinalDirection.NORTH)
    )
    assert len(visible_north) == 3
    assert set(visible_north) == {Vector2D(0, 2), Vector2D(1, 2), Vector2D(2, 2)}
    visible_east = list(
        tree_height_map.visible_trees(looking_direction=CardinalDirection.EAST)
    )
    assert len(visible_east) == 9
    assert set(visible_east) == {Vector2D(i, j) for i in range(3) for j in range(3)}


@pytest.mark.parametrize(
    "position, looking_direction, expected",
    [
        (Vector2D(0, 0), CardinalDirection.WEST, 0),
        (Vector2D(2, 1), CardinalDirection.NORTH, 1),
        (Vector2D(4, 0), CardinalDirection.SOUTH, 3),
    ],
)
def test_tree_height_map_iterates_through_trees_visible_from_given_position_and_direction(
    position, looking_direction, expected
):
    tree_height_map = TreeHeightMap(
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ]
    )
    visible_north = list(
        tree_height_map.visible_trees_from_position(position, looking_direction)
    )
    assert expected == len(visible_north)
