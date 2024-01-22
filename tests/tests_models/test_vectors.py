from models.vectors import CardinalDirection, Vector2D, TurnDirection


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
