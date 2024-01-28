import pytest
from models.vectors import Vector2D, TurnDirection
from models.aoc_2018 import MineCarts

no_carts_layout = "\n".join(
    [
        "/----\\",
        "|    |",
        "|    |",
        "\\----/",
    ]
)
no_intersection_layout = "\n".join(
    [
        "/->--\\",
        "|    v",
        "^    |",
        "\\-<--/",
    ]
)

intersection_layout = "\n".join(
    [
        "/->-\        ",
        "|   |  /----\\",
        "| /-+--+-\  |",
        "| | |  | v  |",
        "\-+-/  \-+--/",
        "  \------/   ",
    ]
)


def test_mine_with_no_carts_stores_zero_positions():
    mine = MineCarts(mine_layout=no_carts_layout)
    assert set(mine.cart_positions) == set()


def test_mine_stores_each_cart_position():
    mine = MineCarts(mine_layout=no_intersection_layout)
    assert set(mine.cart_positions) == {
        Vector2D(2, 0),
        Vector2D(5, 1),
        Vector2D(0, 2),
        Vector2D(2, 3),
    }


def test_mine_carts_can_move_in_a_straight_line():
    mine = MineCarts(mine_layout=no_intersection_layout)
    mine.tick()
    assert set(mine.cart_positions) == {
        Vector2D(3, 0),
        Vector2D(5, 2),
        Vector2D(0, 1),
        Vector2D(1, 3),
    }


def test_mine_carts_can_make_turns():
    mine = MineCarts(mine_layout=no_intersection_layout)
    for _ in range(3):
        mine.tick()
    assert set(mine.cart_positions) == {
        Vector2D(5, 0),
        Vector2D(4, 3),
        Vector2D(1, 0),
        Vector2D(0, 2),
    }


def test_carts_make_predetermined_sequence_of_moves_at_intersections():
    mine = MineCarts(
        mine_layout=intersection_layout,
        intersection_sequence=[
            TurnDirection.LEFT,
            TurnDirection.NO_TURN,
            TurnDirection.RIGHT,
        ],
    )
    for _ in range(13):
        mine.tick()
    assert set(mine.cart_positions) == {Vector2D(7, 2), Vector2D(7, 4)}
    mine.tick()
    assert set(mine.cart_positions) == {Vector2D(7, 3)}


@pytest.mark.parametrize(
    "layout, expected_collisions",
    [
        (intersection_layout, [Vector2D(7, 3)]),
        ("-->-<--><---", [Vector2D(3, 0), Vector2D(8, 0)]),
        ("--<<-->>---", [Vector2D(7, 0)]),
        ("-------^--v\n->>----^--^", [Vector2D(10, 1), Vector2D(2, 1)]),
    ],
)
def test_cart_collisions_are_returned(layout, expected_collisions):
    mine = MineCarts(
        mine_layout=layout,
        intersection_sequence=[
            TurnDirection.LEFT,
            TurnDirection.NO_TURN,
            TurnDirection.RIGHT,
        ],
    )
    collisions = mine.collisions()
    for collision in expected_collisions:
        assert next(collisions) == collision


def test_crashed_carts_are_removed():
    mine = MineCarts(
        mine_layout="->->-<--<",
        intersection_sequence=[
            TurnDirection.LEFT,
            TurnDirection.NO_TURN,
            TurnDirection.RIGHT,
        ],
    )
    collisions = mine.collisions()
    assert list(collisions) == [Vector2D(4, 0), Vector2D(5, 0)]
