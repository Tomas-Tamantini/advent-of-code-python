import pytest
from typing import Iterator
from models.common.vectors import Vector3D
from .hyper_game_of_life import HyperGameOfLife


def _generate_neighbors(cube: Vector3D, num_neighbors: int) -> Iterator[Vector3D]:
    generator = cube.adjacent_positions()
    for _ in range(num_neighbors):
        yield next(generator)


def _cube_with_neighbors(cube: Vector3D, num_neighbors: int) -> set[Vector3D]:
    return {cube, *_generate_neighbors(cube, num_neighbors)}


@pytest.mark.parametrize("num_neighbors", [0, 1, 4, 5, 26])
def test_active_cube_with_less_than_two_or_more_than_three_neighbors_becomes_inactive(
    num_neighbors,
):
    cube = Vector3D(0, 0, 0)
    active_cubes = _cube_with_neighbors(cube, num_neighbors)
    automaton = HyperGameOfLife()
    next_active = automaton.next_state(active_cubes)
    assert cube not in next_active


@pytest.mark.parametrize("num_neighbors", [2, 3])
def test_active_cube_with_two_or_three_neighbors_remains_active(num_neighbors):
    cube = Vector3D(0, 0, 0)
    active_cubes = _cube_with_neighbors(cube, num_neighbors)
    automaton = HyperGameOfLife()
    next_active = automaton.next_state(active_cubes)
    assert cube in next_active


@pytest.mark.parametrize("num_neighbors", [0, 1, 2, 4, 5, 26])
def test_inactive_cube_with_any_number_of_neighbors_other_than_three_remains_inactive(
    num_neighbors,
):
    cube = Vector3D(0, 0, 0)
    active_cubes = set(_generate_neighbors(cube, num_neighbors))
    automaton = HyperGameOfLife()
    next_active = automaton.next_state(active_cubes)
    assert cube not in next_active


def test_inactive_cube_with_three_neighbors_becomes_active():
    cube = Vector3D(0, 0, 0)
    active_cubes = set(_generate_neighbors(cube, num_neighbors=3))
    automaton = HyperGameOfLife()
    next_active = automaton.next_state(active_cubes)
    assert cube in next_active


def test_hyper_game_of_life_updates_all_cubes_at_once():
    active_cubes = {
        Vector3D(1, 0, 0),
        Vector3D(2, 1, 0),
        Vector3D(0, 2, 0),
        Vector3D(1, 2, 0),
        Vector3D(2, 2, 0),
    }
    next_active = HyperGameOfLife().next_state(active_cubes)
    assert len(next_active) == 11
