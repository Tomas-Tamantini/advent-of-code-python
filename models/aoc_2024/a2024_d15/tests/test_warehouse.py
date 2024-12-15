import pytest

from models.common.vectors import CardinalDirection, Vector2D

from ..logic import SingleWidthBox, Warehouse, WarehouseBoxes


@pytest.mark.parametrize(
    ("direction", "expected_position"),
    [
        (CardinalDirection.NORTH, Vector2D(1, 0)),
        (CardinalDirection.SOUTH, Vector2D(1, 2)),
        (CardinalDirection.EAST, Vector2D(2, 1)),
        (CardinalDirection.WEST, Vector2D(0, 1)),
    ],
)
def test_warehouse_robot_can_move_in_four_directions(
    direction: CardinalDirection, expected_position: Vector2D
):
    warehouse = Warehouse(
        robot=Vector2D(1, 1), boxes=WarehouseBoxes(set()), walls=set()
    )
    next_state = warehouse.move_robot(direction)
    assert expected_position == next_state.robot


def test_warehouse_robot_cannot_run_into_walls():
    warehouse = Warehouse(
        robot=Vector2D(1, 1), boxes=WarehouseBoxes(set()), walls={Vector2D(1, 0)}
    )
    next_state = warehouse.move_robot(CardinalDirection.NORTH)
    assert warehouse.robot == next_state.robot


def test_warehouse_robot_pushes_box_in_front_of_it():
    warehouse = Warehouse(
        robot=Vector2D(1, 1),
        boxes=WarehouseBoxes({SingleWidthBox(Vector2D(1, 2))}),
        walls=set(),
    )
    next_state = warehouse.move_robot(CardinalDirection.SOUTH)
    assert next_state.robot == Vector2D(1, 2)
    assert set(next_state.box_positions()) == {Vector2D(1, 3)}


def test_box_pushes_box_in_front_of_it():
    warehouse = Warehouse(
        robot=Vector2D(1, 1),
        boxes=WarehouseBoxes(
            {SingleWidthBox(Vector2D(1, 2)), SingleWidthBox(Vector2D(1, 3))}
        ),
        walls=set(),
    )
    next_state = warehouse.move_robot(CardinalDirection.SOUTH)
    assert next_state.robot == Vector2D(1, 2)
    assert set(next_state.box_positions()) == {Vector2D(1, 3), Vector2D(1, 4)}


def test_box_cannot_run_into_wall():
    warehouse = Warehouse(
        robot=Vector2D(1, 1),
        boxes=WarehouseBoxes(
            {SingleWidthBox(Vector2D(1, 2)), SingleWidthBox(Vector2D(1, 3))}
        ),
        walls={Vector2D(1, 4)},
    )
    next_state = warehouse.move_robot(CardinalDirection.SOUTH)
    assert next_state == warehouse
