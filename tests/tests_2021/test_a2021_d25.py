from models.aoc_2021 import SeaCucumbers, SeaCucumbersHerds
from models.vectors import Vector2D
from models.char_grid import CharacterGrid


def test_sea_cucumbers_only_move_if_space_in_front_is_empty():
    sea_cucumbers = SeaCucumbers(width=3, height=1)
    inital_herds = SeaCucumbersHerds(
        east_facing={Vector2D(0, 0), Vector2D(1, 0)}, south_facing=set()
    )
    next_herds = SeaCucumbersHerds(
        east_facing={Vector2D(0, 0), Vector2D(2, 0)}, south_facing=set()
    )
    assert sea_cucumbers.next_state(inital_herds) == next_herds


def test_east_facing_sea_cucumbers_move_before_south_facing_ones():
    sea_cucumbers = SeaCucumbers(width=100, height=100)
    inital_herds = SeaCucumbersHerds(
        east_facing={Vector2D(0, 0), Vector2D(6, 1)},
        south_facing={Vector2D(1, 0), Vector2D(6, 0)},
    )
    next_herds = SeaCucumbersHerds(
        east_facing={Vector2D(0, 0), Vector2D(7, 1)},
        south_facing={Vector2D(1, 1), Vector2D(6, 1)},
    )
    assert sea_cucumbers.next_state(inital_herds) == next_herds


def test_sea_cucumbers_that_move_off_right_edge_of_grid_wrap_around_to_left_edge():
    sea_cucumbers = SeaCucumbers(width=4, height=2)
    inital_herds = SeaCucumbersHerds(
        east_facing={Vector2D(0, 0), Vector2D(3, 0), Vector2D(3, 1)}, south_facing=set()
    )
    next_herds = SeaCucumbersHerds(
        east_facing={Vector2D(1, 0), Vector2D(3, 0), Vector2D(0, 1)}, south_facing=set()
    )
    assert sea_cucumbers.next_state(inital_herds) == next_herds


def test_sea_cucumbers_that_move_off_bottom_edge_of_grid_wrap_around_to_top_edge():
    sea_cucumbers = SeaCucumbers(width=2, height=4)
    inital_herds = SeaCucumbersHerds(
        east_facing=set(), south_facing={Vector2D(0, 0), Vector2D(0, 3), Vector2D(1, 3)}
    )
    next_herds = SeaCucumbersHerds(
        east_facing=set(), south_facing={Vector2D(0, 1), Vector2D(0, 3), Vector2D(1, 0)}
    )
    assert sea_cucumbers.next_state(inital_herds) == next_herds


def test_sea_cucumbers_stop_moving_after_certain_number_of_steps():
    intial_config = """
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
    """
    grid = CharacterGrid(intial_config)
    sea_cucumbers = SeaCucumbers(width=grid.width, height=grid.height)
    herds = SeaCucumbersHerds(
        east_facing=set(grid.positions_with_value(">")),
        south_facing=set(grid.positions_with_value("v")),
    )
    num_steps = sea_cucumbers.num_steps_until_halt(herds)
    assert num_steps == 58
