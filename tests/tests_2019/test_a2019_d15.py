from models.common.vectors import Vector2D, CardinalDirection
from models.aoc_2019.a2019_d15 import (
    DroidExploredArea,
    CellType,
    RepairDroid,
    RepairDroidIO,
    repair_droid_explore_area,
)


def test_explored_area_starts_empty():
    area = DroidExploredArea()
    assert area.explored_cells == set()


def test_can_add_cells_to_droid_explored_area():
    area = DroidExploredArea()
    area.set_cell(Vector2D(123, 321), CellType.EMPTY)
    area.set_cell(Vector2D(10, 20), CellType.WALL)
    area.set_cell(Vector2D(30, 40), CellType.OXYGEN_SYSTEM)
    assert area.explored_cells == {
        Vector2D(123, 321),
        Vector2D(10, 20),
        Vector2D(30, 40),
    }
    assert area.empty_cells == {Vector2D(123, 321), Vector2D(30, 40)}
    assert area.position_oxygen_system == Vector2D(30, 40)


def test_explored_area_indicates_smallest_distance_to_oxygen_system():
    area = DroidExploredArea()
    for i in range(3):
        for j in range(4):
            area.set_cell(Vector2D(i, j), CellType.EMPTY)
    area.set_cell(Vector2D(2, 1), CellType.OXYGEN_SYSTEM)
    assert area.distance_to_oxygen_system(starting_point=Vector2D(0, 1)) == 2
    area.set_cell(Vector2D(1, 1), CellType.WALL)
    area.set_cell(Vector2D(1, 2), CellType.WALL)
    assert area.distance_to_oxygen_system(starting_point=Vector2D(0, 1)) == 4


def test_explored_area_indicates_time_to_fill_with_oxygen():
    area = DroidExploredArea()
    for i in range(10):
        for j in range(10):
            cell_type = (
                CellType.WALL
                if i == 0 or j == 0 or i == 9 or j == 9
                else CellType.EMPTY
            )
            area.set_cell(Vector2D(i, j), cell_type)
    area.set_cell(Vector2D(1, 1), CellType.OXYGEN_SYSTEM)
    assert area.minutes_to_fill_with_oxygen() == 14


def test_repair_droid_can_move_in_some_direction():
    droid = RepairDroid(initial_position=Vector2D(123, 321))
    droid.move(CardinalDirection.NORTH)
    assert droid.position == Vector2D(123, 322)


def test_repair_droid_can_backtrack():
    droid = RepairDroid(initial_position=Vector2D(0, 0))
    droid.move(CardinalDirection.NORTH)
    droid.move(CardinalDirection.EAST)
    assert droid.backtrack_direction() == CardinalDirection.WEST
    droid.move(droid.backtrack_direction())
    assert droid.backtrack_direction() == CardinalDirection.SOUTH
    droid.move(droid.backtrack_direction())
    assert droid.position == Vector2D(0, 0)


def test_repair_droid_backtrack_direction_returns_none_if_no_backtrack_possible():
    droid = RepairDroid()
    assert droid.backtrack_direction() is None


def test_repair_droid_first_position_is_empty():
    droid = RepairDroid(initial_position=Vector2D(123, 321))
    area = DroidExploredArea()
    _ = RepairDroidIO(droid, area)
    assert area.empty_cells == {Vector2D(123, 321)}


def test_droid_output_value_0_means_wall():
    area = DroidExploredArea()
    droid = RepairDroid()
    io = RepairDroidIO(droid, area)
    io.read()
    io.write(value=0)
    assert area.explored_cells == {Vector2D(0, 0), Vector2D(0, 1)}
    assert area.empty_cells == {Vector2D(0, 0)}


def test_droid_output_value_1_means_empty():
    area = DroidExploredArea()
    droid = RepairDroid()
    io = RepairDroidIO(droid, area)
    io.read()
    io.write(value=1)
    assert area.explored_cells == {Vector2D(0, 0), Vector2D(0, 1)}
    assert area.empty_cells == {Vector2D(0, 0), Vector2D(0, 1)}


def test_droid_output_value_2_means_oxygen_system():
    area = DroidExploredArea()
    droid = RepairDroid()
    io = RepairDroidIO(droid, area)
    io.read()
    io.write(value=2)
    assert area.explored_cells == {Vector2D(0, 0), Vector2D(0, 1)}
    assert area.empty_cells == {Vector2D(0, 0), Vector2D(0, 1)}
    assert area.position_oxygen_system == Vector2D(0, 1)


def test_can_explore_area_with_intcode_program():
    area = DroidExploredArea()
    instructions = [3, 500, 104, 0, 1106, 0, 0]  # Outputs wall in all directions
    repair_droid_explore_area(area, instructions)
    assert area.explored_cells == {
        Vector2D(0, 0),
        Vector2D(0, 1),
        Vector2D(0, -1),
        Vector2D(1, 0),
        Vector2D(-1, 0),
    }
    assert area.empty_cells == {Vector2D(0, 0)}
