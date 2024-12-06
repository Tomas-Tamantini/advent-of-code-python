from typing import Iterator

import pytest

from models.common.vectors import CanonicalHexagonalCoordinates

from ..hexagonal_automaton import HexagonalAutomaton


def _generate_neighbors(
    tile: CanonicalHexagonalCoordinates, num_neighbors: int
) -> Iterator[CanonicalHexagonalCoordinates]:
    generator = tile.adjacent_positions()
    for _ in range(num_neighbors):
        yield next(generator)


def _tile_with_neighbors(
    tile: CanonicalHexagonalCoordinates, num_neighbors: int
) -> set[CanonicalHexagonalCoordinates]:
    return {tile, *_generate_neighbors(tile, num_neighbors)}


@pytest.mark.parametrize("num_neighbors", [0, 3, 4, 5, 6])
def test_hexagonal_automaton_active_tile_with_less_than_one_or_more_than_two_neighbors_becomes_inactive(
    num_neighbors,
):
    tile = CanonicalHexagonalCoordinates(0, 0)
    active_tiles = _tile_with_neighbors(tile, num_neighbors)
    automaton = HexagonalAutomaton()
    next_active = automaton.next_state(active_tiles)
    assert tile not in next_active


@pytest.mark.parametrize("num_neighbors", [1, 2])
def test_hexagonal_automaton_active_tile_with_one_or_two_neighbors_remains_active(
    num_neighbors,
):
    tile = CanonicalHexagonalCoordinates(0, 0)
    active_tiles = _tile_with_neighbors(tile, num_neighbors)
    automaton = HexagonalAutomaton()
    next_active = automaton.next_state(active_tiles)
    assert tile in next_active


@pytest.mark.parametrize("num_neighbors", [0, 1, 3, 4, 5, 6])
def test_hexagonal_automaton_inactive_tile_with_any_number_of_neighbors_other_than_two_remains_inactive(
    num_neighbors,
):
    tile = CanonicalHexagonalCoordinates(0, 0)
    active_tiles = set(_generate_neighbors(tile, num_neighbors))
    automaton = HexagonalAutomaton()
    next_active = automaton.next_state(active_tiles)
    assert tile not in next_active


def test_hexagonal_automaton_inactive_tile_with_two_neighbors_becomes_active():
    tile = CanonicalHexagonalCoordinates(0, 0)
    active_tiles = set(_generate_neighbors(tile, num_neighbors=2))
    automaton = HexagonalAutomaton()
    next_active = automaton.next_state(active_tiles)
    assert tile in next_active


def test_hexagonal_automaton_updates_all_tiles_at_once():
    active_tiles = {
        CanonicalHexagonalCoordinates(1, 0),
        CanonicalHexagonalCoordinates(2, 1),
        CanonicalHexagonalCoordinates(0, 2),
        CanonicalHexagonalCoordinates(1, 2),
        CanonicalHexagonalCoordinates(2, 2),
    }
    next_active = HexagonalAutomaton().next_state(active_tiles)
    assert len(next_active) == 8
