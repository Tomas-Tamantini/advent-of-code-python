from models.aoc_2015 import GameOfLife


def test_cell_which_is_off_and_has_less_than_3_neighbors_stays_off():
    game = GameOfLife(3, 3)
    assert (1, 1) not in game.step(set())
    assert (1, 1) not in game.step({(0, 0)})
    assert (1, 1) not in game.step({(0, 0), (0, 1)})


def test_cell_which_is_off_and_has_more_than_3_neighbors_stays_off():
    game = GameOfLife(3, 3)
    assert (1, 1) not in game.step({(0, 0), (0, 1), (0, 2), (1, 0)})
    assert (1, 1) not in game.step({(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)})


def test_cell_which_is_on_and_has_less_than_two_neighbors_dies():
    game = GameOfLife(3, 3)
    assert (1, 1) not in game.step({(1, 1)})
    assert (1, 1) not in game.step({(1, 1), (0, 0)})


def test_cell_which_is_on_and_has_more_than_three_neighbors_dies():
    game = GameOfLife(3, 3)
    assert (1, 1) not in game.step({(1, 1), (0, 0), (0, 1), (0, 2), (1, 0)})
    assert (1, 1) not in game.step({(1, 1), (0, 0), (0, 1), (0, 2), (1, 0), (2, 0)})


def test_cell_which_is_on_and_has_two_or_three_neighbors_survives():
    game = GameOfLife(3, 3)
    assert (1, 1) in game.step({(1, 1), (0, 0), (0, 1)})
    assert (1, 1) in game.step({(1, 1), (0, 0), (0, 1), (0, 2)})


def test_cell_which_is_off_and_has_three_neighbors_comes_alive():
    game = GameOfLife(3, 3)
    assert (1, 1) in game.step({(0, 0), (0, 1), (2, 2)})


def test_cell_outside_grid_never_comes_alive():
    game = GameOfLife(3, 3)
    assert (3, 1) not in game.step({(2, 0), (2, 1), (2, 2)})


def test_can_force_cells_to_be_always_on():
    game = GameOfLife(3, 3)
    new_cells = game.step_with_always_on_cells(
        live_cells=set(),
        always_on_cells={(0, 0), (2, 2), (0, 2)},
    )
    assert {(1, 1), (0, 0), (2, 2), (0, 2)} == new_cells


def test_can_get_corner_cells():
    game = GameOfLife(3, 3)
    assert {(0, 0), (2, 0), (0, 2), (2, 2)} == set(game.corner_cells)
