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
