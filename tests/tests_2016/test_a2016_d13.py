import pytest
from models.aoc_2016 import MazeCubicle, is_wall
from models.vectors import Vector2D


def test_follows_proper_calculation_to_check_if_cubicle_is_wall():
    assert is_wall(Vector2D(5, 2), 10) is True
    assert is_wall(Vector2D(5, 3), 10) is False
    assert is_wall(Vector2D(6, 2), 10) is True
    assert is_wall(Vector2D(6, 3), 10) is True


def test_if_path_cannot_be_found_value_error_is_raised():
    is_wall_calculator = lambda _: True
    MazeCubicle.is_wall = is_wall_calculator
    MazeCubicle.destination = Vector2D(1, 1)
    maze = MazeCubicle(position=Vector2D(0, 0))
    with pytest.raises(ValueError):
        maze.length_shortest_path()


def test_if_origin_and_destination_are_the_same_shortest_path_length_is_zero():
    is_wall_calculator = lambda _: False
    MazeCubicle.is_wall = is_wall_calculator
    MazeCubicle.destination = Vector2D(1, 1)
    maze = MazeCubicle(position=Vector2D(1, 1))
    assert maze.length_shortest_path() == 0


def test_if_no_walls_exist_shortest_path_length_is_manhattan_distance():
    is_wall_calculator = lambda _: False
    MazeCubicle.is_wall = is_wall_calculator
    MazeCubicle.destination = Vector2D(5, 7)
    maze = MazeCubicle(position=Vector2D(1, 2))
    assert maze.length_shortest_path() == 9


def test_shortest_path_that_does_not_go_through_negative_coordinates_is_found():
    def is_wall_calculator(position: Vector2D) -> bool:
        return position.y not in (-1, 1_000) and position.x not in (0, 10)

    MazeCubicle.is_wall = is_wall_calculator
    MazeCubicle.destination = Vector2D(10, 0)
    maze = MazeCubicle(position=Vector2D(0, 0))
    # Cannot take shortcut through y = -1, so needs to go up to y = 1000
    assert maze.length_shortest_path() == 2010


def test_number_of_reachable_cubicles_in_maze_without_walls_is_centered_square_numbers():
    MazeCubicle.is_wall = lambda _: False
    maze = MazeCubicle(position=Vector2D(100, 100))
    assert maze.number_of_reachable_cubicles(0) == 1
    assert maze.number_of_reachable_cubicles(1) == 5
    assert maze.number_of_reachable_cubicles(2) == 13


def test_number_of_reachable_cubicles_starting_at_origin_in_maze_without_walls_is_triangular_numbers():
    MazeCubicle.is_wall = lambda _: False
    maze = MazeCubicle(position=Vector2D(0, 0))
    assert maze.number_of_reachable_cubicles(0) == 1
    assert maze.number_of_reachable_cubicles(1) == 3
    assert maze.number_of_reachable_cubicles(2) == 6


def test_number_of_reachable_cubicles_in_tunnel_maze_grows_linearly_after_first_few_steps():
    MazeCubicle.is_wall = lambda pos: pos.x not in (0, 1, 2)
    maze = MazeCubicle(position=Vector2D(0, 0))
    assert maze.number_of_reachable_cubicles(0) == 1
    assert maze.number_of_reachable_cubicles(1) == 3
    assert maze.number_of_reachable_cubicles(2) == 6
    assert maze.number_of_reachable_cubicles(3) == 9
    assert maze.number_of_reachable_cubicles(4) == 12
    assert maze.number_of_reachable_cubicles(5) == 15
