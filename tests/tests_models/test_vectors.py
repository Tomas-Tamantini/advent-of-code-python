import pytest
from models.vectors import CardinalDirection, Vector2D, TurnDirection, BoundingBox


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


def test_bounding_box_dimensions_are_calculated_properly():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.width == 3
    assert bounding_box.height == 4
    assert bounding_box.area == 12


def test_bounding_box_of_zero_points_has_all_dimensions_zero():
    bounding_box = BoundingBox.from_points([])
    assert bounding_box.width == bounding_box.height == bounding_box.area == 0


def test_bounding_box_of_multiple_points_is_smallest_possible():
    points = [
        Vector2D(100, 1000),
        Vector2D(200, 2000),
        Vector2D(200, 1000),
        Vector2D(150, 1500),
    ]
    bounding_box = BoundingBox.from_points(points)
    assert bounding_box == BoundingBox(Vector2D(100, 1000), Vector2D(200, 2000))
