from models.common.vectors import Vector2D

from .game_of_life_lights import GameOfLifeLights


def test_cell_which_is_off_and_has_less_than_3_neighbors_stays_off():
    game = GameOfLifeLights(3, 3)
    assert Vector2D(1, 1) not in game.next_state(set())
    assert Vector2D(1, 1) not in game.next_state({Vector2D(0, 0)})
    assert Vector2D(1, 1) not in game.next_state({Vector2D(0, 0), Vector2D(0, 1)})


def test_cell_which_is_off_and_has_more_than_3_neighbors_stays_off():
    game = GameOfLifeLights(3, 3)
    assert Vector2D(1, 1) not in game.next_state(
        {Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 0)}
    )
    assert Vector2D(1, 1) not in game.next_state(
        {Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 0), Vector2D(2, 0)}
    )


def test_cell_which_is_on_and_has_less_than_two_neighbors_dies():
    game = GameOfLifeLights(3, 3)
    assert Vector2D(1, 1) not in game.next_state({Vector2D(1, 1)})
    assert Vector2D(1, 1) not in game.next_state({Vector2D(1, 1), Vector2D(0, 0)})


def test_cell_which_is_on_and_has_more_than_three_neighbors_dies():
    game = GameOfLifeLights(3, 3)
    assert Vector2D(1, 1) not in game.next_state(
        {Vector2D(1, 1), Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 0)}
    )
    assert Vector2D(1, 1) not in game.next_state(
        {
            Vector2D(1, 1),
            Vector2D(0, 0),
            Vector2D(0, 1),
            Vector2D(0, 2),
            Vector2D(1, 0),
            Vector2D(2, 0),
        }
    )


def test_cell_which_is_on_and_has_two_or_three_neighbors_survives():
    game = GameOfLifeLights(3, 3)
    assert Vector2D(1, 1) in game.next_state(
        {Vector2D(1, 1), Vector2D(0, 0), Vector2D(0, 1)}
    )
    assert Vector2D(1, 1) in game.next_state(
        {Vector2D(1, 1), Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2)}
    )


def test_cell_which_is_off_and_has_three_neighbors_comes_alive():
    game = GameOfLifeLights(3, 3)
    assert Vector2D(1, 1) in game.next_state(
        {Vector2D(0, 0), Vector2D(0, 1), Vector2D(2, 2)}
    )


def test_cell_outside_grid_never_comes_alive():
    game = GameOfLifeLights(3, 3)
    assert (3, 1) not in game.next_state(
        {Vector2D(2, 0), Vector2D(2, 1), Vector2D(2, 2)}
    )


def test_can_force_cells_to_be_always_on():
    game = GameOfLifeLights(3, 3)
    new_cells = game.step_with_always_on_cells(
        live_cells=set(),
        always_on_cells={Vector2D(0, 0), Vector2D(2, 2), Vector2D(0, 2)},
    )
    assert {Vector2D(1, 1), Vector2D(0, 0), Vector2D(2, 2), Vector2D(0, 2)} == new_cells


def test_can_get_corner_cells():
    game = GameOfLifeLights(3, 3)
    assert {Vector2D(0, 0), Vector2D(2, 0), Vector2D(0, 2), Vector2D(2, 2)} == set(
        game.corner_cells
    )
