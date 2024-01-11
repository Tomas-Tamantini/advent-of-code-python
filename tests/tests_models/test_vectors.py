from models.vectors import CardinalDirection, Vector2D


def test_vector_moves_by_one_step_by_default():
    assert Vector2D(0, 0).move(CardinalDirection.NORTH) == Vector2D(0, 1)
    assert Vector2D(0, 0).move(CardinalDirection.EAST) == Vector2D(1, 0)
    assert Vector2D(0, 0).move(CardinalDirection.SOUTH) == Vector2D(0, -1)
    assert Vector2D(0, 0).move(CardinalDirection.WEST) == Vector2D(-1, 0)


def test_vector_can_move_specified_number_of_steps():
    assert Vector2D(10, 10).move(CardinalDirection.NORTH, 5) == Vector2D(10, 15)


def test_cardinal_directions_can_be_spun_around():
    assert CardinalDirection.NORTH.turn_left() == CardinalDirection.WEST
    assert CardinalDirection.WEST.turn_left() == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn_left() == CardinalDirection.EAST
    assert CardinalDirection.EAST.turn_left() == CardinalDirection.NORTH

    assert CardinalDirection.NORTH.turn_right() == CardinalDirection.EAST
    assert CardinalDirection.EAST.turn_right() == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn_right() == CardinalDirection.WEST
    assert CardinalDirection.WEST.turn_right() == CardinalDirection.NORTH