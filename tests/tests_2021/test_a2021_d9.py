from models.char_grid import CharacterGrid
from models.vectors import Vector2D
from models.aoc_2021 import SmokeBasin


def _example_basin() -> SmokeBasin:
    grid = CharacterGrid(
        text="""2199943210
            3987894921
            9856789892
            8767896789
            9899965678"""
    )
    return SmokeBasin(
        heightmap={pos: int(height) for pos, height in grid.tiles.items()}
    )


def test_smoke_basin_local_minima_are_points_strictly_lower_than_all_four_neighbors():
    basin = _example_basin()
    local_minima = list(basin.local_minima())
    assert len(local_minima) == 4
    assert set(local_minima) == {
        (Vector2D(1, 0), 1),
        (Vector2D(9, 0), 0),
        (Vector2D(2, 2), 5),
        (Vector2D(6, 4), 5),
    }
