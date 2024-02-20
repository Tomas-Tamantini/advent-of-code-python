import pytest
from models.vectors import (
    CardinalDirection,
    Vector2D,
    TurnDirection,
    BoundingBox,
    Vector3D,
)


def test_can_get_manhattan_distance_for_vector_2d():
    assert Vector2D(1, 2).manhattan_distance(Vector2D(4, -3)) == 8


def test_can_get_manhattan_size_for_vector_2d():
    assert Vector2D(1, -2).manhattan_size == 3


def test_vectors_can_be_added_together():
    assert Vector2D(1, 2) + Vector2D(3, 4) == Vector2D(4, 6)


def test_vectors_can_be_subtracted_from_each_other():
    assert Vector2D(1, 2) - Vector2D(3, 4) == Vector2D(-2, -2)


def test_vectors_can_be_multiplied_by_a_scalar():
    assert Vector2D(1, 2) * 3 == 3 * Vector2D(1, 2) == Vector2D(3, 6)


def test_vector_moves_by_one_step_by_default():
    assert Vector2D(0, 0).move(CardinalDirection.NORTH) == Vector2D(0, 1)
    assert Vector2D(0, 0).move(CardinalDirection.EAST) == Vector2D(1, 0)
    assert Vector2D(0, 0).move(CardinalDirection.SOUTH) == Vector2D(0, -1)
    assert Vector2D(0, 0).move(CardinalDirection.WEST) == Vector2D(-1, 0)


def test_vector_can_move_specified_number_of_steps():
    assert Vector2D(10, 10).move(CardinalDirection.NORTH, 5) == Vector2D(10, 15)


def test_vector_can_specify_direction_of_y_axis():
    assert Vector2D(10, 10).move(
        CardinalDirection.NORTH, y_grows_down=True
    ) == Vector2D(10, 9)
    assert Vector2D(10, 10).move(
        CardinalDirection.SOUTH, y_grows_down=True
    ) == Vector2D(10, 11)


def test_can_find_all_adjacent_positions_not_including_diagonal_by_default():
    assert set(Vector2D(0, 0).adjacent_positions()) == {
        Vector2D(0, 1),
        Vector2D(1, 0),
        Vector2D(0, -1),
        Vector2D(-1, 0),
    }


def test_can_find_all_adjacent_positions_including_diagonal():
    assert set(Vector2D(0, 0).adjacent_positions(include_diagonals=True)) == {
        Vector2D(0, 1),
        Vector2D(1, 0),
        Vector2D(0, -1),
        Vector2D(-1, 0),
        Vector2D(1, 1),
        Vector2D(1, -1),
        Vector2D(-1, -1),
        Vector2D(-1, 1),
    }


def test_cardinal_directions_are_vertical_or_horizontal():
    assert CardinalDirection.NORTH.is_vertical
    assert CardinalDirection.SOUTH.is_vertical
    assert not CardinalDirection.EAST.is_vertical
    assert not CardinalDirection.WEST.is_vertical

    assert CardinalDirection.EAST.is_horizontal
    assert CardinalDirection.WEST.is_horizontal
    assert not CardinalDirection.NORTH.is_horizontal
    assert not CardinalDirection.SOUTH.is_horizontal


def test_cardinal_directions_can_be_spun_around():
    assert CardinalDirection.NORTH.turn_left() == CardinalDirection.WEST
    assert CardinalDirection.WEST.turn_left() == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn_left() == CardinalDirection.EAST
    assert CardinalDirection.EAST.turn_left() == CardinalDirection.NORTH

    assert CardinalDirection.NORTH.turn_right() == CardinalDirection.EAST
    assert CardinalDirection.EAST.turn_right() == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn_right() == CardinalDirection.WEST
    assert CardinalDirection.WEST.turn_right() == CardinalDirection.NORTH

    assert CardinalDirection.NORTH.reverse() == CardinalDirection.SOUTH
    assert CardinalDirection.EAST.reverse() == CardinalDirection.WEST
    assert CardinalDirection.SOUTH.reverse() == CardinalDirection.NORTH
    assert CardinalDirection.WEST.reverse() == CardinalDirection.EAST

    assert (
        CardinalDirection.NORTH.turn(TurnDirection.NO_TURN) == CardinalDirection.NORTH
    )
    assert CardinalDirection.WEST.turn(TurnDirection.LEFT) == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn(TurnDirection.RIGHT) == CardinalDirection.WEST
    assert CardinalDirection.EAST.turn(TurnDirection.U_TURN) == CardinalDirection.WEST


def test_bottom_left_cannot_be_to_the_right_of_top_right():
    with pytest.raises(ValueError):
        BoundingBox(Vector2D(2, 0), Vector2D(1, 0))


def test_bottom_left_cannot_be_to_the_top_of_top_right():
    with pytest.raises(ValueError):
        BoundingBox(Vector2D(0, 2), Vector2D(0, 1))


def test_bounding_box_with_bottom_left_equal_to_top_right_has_all_dimensions_zero():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(1, 2))
    assert bounding_box.width == bounding_box.height == bounding_box.area == 0


def test_bounding_box_has_min_and_max_x_and_y_properties():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.min_x == 1
    assert bounding_box.max_x == 4
    assert bounding_box.min_y == 2
    assert bounding_box.max_y == 6


def test_bounding_box_dimensions_are_calculated_properly():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.width == 3
    assert bounding_box.height == 4
    assert bounding_box.area == 12


def test_bounding_box_of_zero_points_has_all_dimensions_zero():
    bounding_box = BoundingBox.from_points([])
    assert bounding_box.width == bounding_box.height == bounding_box.area == 0


def test_can_check_whether_bounding_box_contains_a_point():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.contains(Vector2D(1, 2))
    assert bounding_box.contains(Vector2D(4, 6))
    assert bounding_box.contains(Vector2D(2, 3))
    assert not bounding_box.contains(Vector2D(0, 2))
    assert not bounding_box.contains(Vector2D(1, 1))
    assert not bounding_box.contains(Vector2D(4, 7))


def test_bounding_box_of_multiple_points_is_smallest_possible():
    points = [
        Vector2D(100, 1000),
        Vector2D(200, 2000),
        Vector2D(200, 1000),
        Vector2D(150, 1500),
    ]
    bounding_box = BoundingBox.from_points(points)
    assert bounding_box == BoundingBox(Vector2D(100, 1000), Vector2D(200, 2000))


def test_intersection_of_two_bounding_boxes_which_do_not_intersect_is_empty():
    box_a = BoundingBox(bottom_left=Vector2D(0, 0), top_right=Vector2D(10, 20))
    box_b = BoundingBox(bottom_left=Vector2D(11, 21), top_right=Vector2D(30, 40))
    assert box_a.intersection(box_b) is None


def test_intersection_of_two_overlapping_bounding_boxes_is_their_common_area():
    box_a = BoundingBox(bottom_left=Vector2D(0, 0), top_right=Vector2D(10, 20))
    box_b = BoundingBox(bottom_left=Vector2D(5, 10), top_right=Vector2D(15, 18))
    assert box_a.intersection(box_b) == BoundingBox(
        bottom_left=Vector2D(5, 10), top_right=Vector2D(10, 18)
    )


def test_can_iterate_through_vector_3d_coordinates():
    vector = Vector3D(x=1, y=2, z=3)
    assert list(vector) == [1, 2, 3]


def test_can_access_vector_3d_coordinates_by_index_and_name():
    vector = Vector3D(x=1, y=2, z=3)
    assert vector.x == vector[0] == 1
    assert vector.y == vector[1] == 2
    assert vector.z == vector[2] == 3


def test_can_get_manhattan_distance_for_vector_3d():
    assert Vector3D(1, 2, 3).manhattan_distance(Vector3D(4, -3, 2)) == 9


def test_can_get_manhattan_size_for_vector_3d():
    assert Vector3D(1, -2, 3).manhattan_size == 6


def test_can_add_vectors_3d_together():
    assert Vector3D(1, 2, 3) + Vector3D(4, 5, 6) == Vector3D(5, 7, 9)


def test_can_subtract_vectors_3d_from_each_other():
    assert Vector3D(1, 2, 3) - Vector3D(3, 2, 1) == Vector3D(-2, 0, 2)
