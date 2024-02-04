import pytest
from models.vectors import Vector2D
from models.aoc_2018 import LumberArea, AcreType

CENTER = Vector2D(1, 1)
area = LumberArea(width=3, height=3)


def test_empty_area_remains_empty():
    assert area.next_state({}) == {}


def _build_cells(
    center_type: AcreType, neighboring_type: AcreType, num_neighbors: int
) -> dict[Vector2D:AcreType]:
    cells = {CENTER: center_type}
    neighbors = CENTER.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        cells[next(neighbors)] = neighboring_type
    return cells


@pytest.mark.parametrize("num_tree_neighbors", [0, 1, 2])
def test_open_acre_with_less_than_three_neighboring_trees_remains_open(
    num_tree_neighbors,
):
    cells = _build_cells(AcreType.OPEN, AcreType.TREE, num_tree_neighbors)
    assert area.next_state(cells)[CENTER] == AcreType.OPEN


@pytest.mark.parametrize("num_tree_neighbors", [3, 4, 8])
def test_open_acre_with_more_than_two_neighboring_trees_becomes_tree(
    num_tree_neighbors,
):
    cells = _build_cells(AcreType.OPEN, AcreType.TREE, num_tree_neighbors)
    assert area.next_state(cells)[CENTER] == AcreType.TREE


@pytest.mark.parametrize("num_lumberyard_neighbors", [0, 1, 2])
def test_tree_acre_with_less_than_three_neighboring_lumberyards_remains_tree(
    num_lumberyard_neighbors,
):
    cells = _build_cells(AcreType.TREE, AcreType.LUMBERYARD, num_lumberyard_neighbors)
    assert area.next_state(cells)[CENTER] == AcreType.TREE


@pytest.mark.parametrize("num_lumberyard_neighbors", [3, 4, 8])
def test_tree_acre_with_more_than_two_neighboring_lumberyards_becomes_lumberyard(
    num_lumberyard_neighbors,
):
    cells = _build_cells(AcreType.TREE, AcreType.LUMBERYARD, num_lumberyard_neighbors)
    assert area.next_state(cells)[CENTER] == AcreType.LUMBERYARD


def test_lumberyard_adjacent_to_tree_and_to_other_lumberyard_remains_lumberyard():
    cells = {
        CENTER: AcreType.LUMBERYARD,
        Vector2D(0, 0): AcreType.TREE,
        Vector2D(2, 2): AcreType.LUMBERYARD,
    }
    assert area.next_state(cells)[CENTER] == AcreType.LUMBERYARD


def test_lumberyard_not_adjacent_to_tree_becomes_open():
    cells = {
        CENTER: AcreType.LUMBERYARD,
        Vector2D(2, 2): AcreType.LUMBERYARD,
    }
    assert area.next_state(cells)[CENTER] == AcreType.OPEN


def test_lumberyard_not_adjacent_to_other_lumberyard_becomes_open():
    cells = {
        CENTER: AcreType.LUMBERYARD,
        Vector2D(2, 2): AcreType.TREE,
    }
    assert area.next_state(cells)[CENTER] == AcreType.OPEN


def test_cell_outside_bounds_is_ignored():
    cells = {Vector2D(i, 0): AcreType.TREE for i in range(3)}
    assert area.next_state(cells)[Vector2D(1, 1)] == AcreType.TREE
    assert area.next_state(cells)[Vector2D(1, -1)] == AcreType.OPEN


def _cells_from_str(s: str) -> dict[Vector2D:AcreType]:
    cells = {}
    for y, row in enumerate(s.splitlines()):
        for x, char in enumerate(row.strip()):
            cells[Vector2D(x, y)] = AcreType(char)
    return cells


SAMPLE_CELLS = _cells_from_str(
    """.#.#...|#.
       .....#|##|
       .|..|...#.
       ..|#.....#
       #.#|||#|#|
       ...#.||...
       .|....|...
       ||...#|.#|
       |.||||..|.
       ...#.|..|."""
)


def test_many_cells_are_updated_simultaneously():
    next_cells = LumberArea(10, 10).next_state(SAMPLE_CELLS)
    assert next_cells == _cells_from_str(
        """.......##.
           ......|###
           .|..|...#.
           ..|#||...#
           ..##||.|#|
           ...#||||..
           ||...|||..
           |||||.||.|
           ||||||||||
           ....||..|."""
    )


def test_can_step_multiple_generations():
    next_cells = LumberArea(10, 10).multi_step(SAMPLE_CELLS, num_steps=10)
    assert next_cells == _cells_from_str(
        """.||##.....
           ||###.....
           ||##......
           |##.....##
           |##.....##
           |##....##|
           ||##.####|
           ||#####|||
           ||||#|||||
           ||||||||||"""
    )


def test_stepping_multiple_generations_is_done_efficiently():

    next_cells = LumberArea(10, 10).multi_step(SAMPLE_CELLS, num_steps=10_000_000_000)
    assert next_cells == _cells_from_str(
        """..........
           ..........
           ..........
           ..........
           ..........
           ..........
           ..........
           ..........
           ..........
           .........."""
    )
