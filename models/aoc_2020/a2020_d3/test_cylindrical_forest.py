import pytest

from models.common.vectors import Vector2D

from .cylindrical_forest import CylindricalForest


def _forest_from_str(s: str) -> CylindricalForest:
    lines = [line.strip() for line in s.strip().split("\n") if line.strip()]
    height = len(lines)
    width = len(lines[0])
    trees = set()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == "#":
                trees.add(Vector2D(x, y))
    return CylindricalForest(width, height, trees)


def test_can_query_whether_cell_in_cylindrical_forest_is_tree():
    forest = _forest_from_str(
        """
        #.
        .#
        ##
        """
    )
    assert forest.is_tree_at(Vector2D(0, 0))
    assert not forest.is_tree_at(Vector2D(1, 0))
    assert not forest.is_tree_at(Vector2D(0, 1))
    assert forest.is_tree_at(Vector2D(1, 1))
    assert forest.is_tree_at(Vector2D(0, 2))
    assert forest.is_tree_at(Vector2D(1, 2))


def test_querying_cell_with_y_value_out_of_bounds_raises_index_error():
    forest = _forest_from_str(
        """
        #.
        .#
        ##
        """
    )
    with pytest.raises(IndexError):
        forest.is_tree_at(Vector2D(0, 3))
    with pytest.raises(IndexError):
        forest.is_tree_at(Vector2D(1, -1))


def test_querying_cell_with_x_value_out_of_bounds_wraps_around_forest():
    forest = _forest_from_str(
        """
        #.
        .#
        ##
        """
    )
    assert forest.is_tree_at(Vector2D(2, 0))
    assert forest.is_tree_at(Vector2D(-1234, 0))
    assert not forest.is_tree_at(Vector2D(3333, 0))


def test_number_of_collisions_with_trees_counts_from_top_left_cell_and_wraps_around_horizontally():
    forest = _forest_from_str(
        """
        ..##.......
        #...#...#..
        .#....#..#.
        ..#.#...#.#
        .#...##..#.
        ..#.##.....
        .#.#.#....#
        .#........#
        #.##...#...
        #...##....#
        .#..#...#.#
        """
    )
    assert (
        forest.number_of_collisions_with_trees(
            steps_right=3,
            steps_down=1,
            starting_point=Vector2D(0, 0),
        )
        == 7
    )
