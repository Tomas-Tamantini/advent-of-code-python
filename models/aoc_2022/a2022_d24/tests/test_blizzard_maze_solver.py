from ..logic import BlizzardMazeSolver, BlizzardValley, Blizzard, BlizzardNavigator
from models.common.vectors import Vector2D, CardinalDirection


def test_blizzard_maze_solver_starts_at_entrance_of_valley():
    valley = BlizzardValley(
        height=3, width=4, entrance=Vector2D(1, 0), exit=Vector2D(2, 2), blizzards=set()
    )
    solver = BlizzardMazeSolver(valley)
    assert solver.first_state() == BlizzardNavigator(position=Vector2D(1, 0), time=0)


def test_blizzard_maze_solver_has_exit_as_terminal_state():
    valley = BlizzardValley(
        height=3, width=4, entrance=Vector2D(1, 0), exit=Vector2D(2, 2), blizzards=set()
    )
    solver = BlizzardMazeSolver(valley)
    assert solver.is_terminal(BlizzardNavigator(position=Vector2D(2, 2), time=123))
    assert not solver.is_terminal(BlizzardNavigator(position=Vector2D(1, 0), time=123))


def test_blizzard_maze_solver_finds_shortest_time_to_reach_exit_without_intercepting_blizzards():
    valley = BlizzardValley(
        height=6,
        width=8,
        entrance=Vector2D(1, 0),
        exit=Vector2D(6, 5),
        blizzards={
            Blizzard(Vector2D(1, 1), CardinalDirection.EAST),
            Blizzard(Vector2D(2, 1), CardinalDirection.EAST),
            Blizzard(Vector2D(1, 3), CardinalDirection.EAST),
            Blizzard(Vector2D(4, 3), CardinalDirection.EAST),
            Blizzard(Vector2D(6, 3), CardinalDirection.EAST),
            Blizzard(Vector2D(6, 4), CardinalDirection.EAST),
            Blizzard(Vector2D(4, 1), CardinalDirection.WEST),
            Blizzard(Vector2D(6, 1), CardinalDirection.WEST),
            Blizzard(Vector2D(2, 2), CardinalDirection.WEST),
            Blizzard(Vector2D(5, 2), CardinalDirection.WEST),
            Blizzard(Vector2D(6, 2), CardinalDirection.WEST),
            Blizzard(Vector2D(5, 3), CardinalDirection.WEST),
            Blizzard(Vector2D(1, 4), CardinalDirection.WEST),
            Blizzard(Vector2D(5, 1), CardinalDirection.NORTH),
            Blizzard(Vector2D(2, 4), CardinalDirection.NORTH),
            Blizzard(Vector2D(4, 4), CardinalDirection.NORTH),
            Blizzard(Vector2D(5, 4), CardinalDirection.NORTH),
            Blizzard(Vector2D(2, 3), CardinalDirection.SOUTH),
            Blizzard(Vector2D(3, 4), CardinalDirection.SOUTH),
        },
    )
    solver = BlizzardMazeSolver(valley)
    assert solver.min_steps_to_exit() == 18
