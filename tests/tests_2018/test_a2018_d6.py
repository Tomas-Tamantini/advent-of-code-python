from math import inf
from models.vectors import Vector2D
from models.aoc_2018 import ManhattanVoronoi


def test_no_point_extends_indefinetely_if_there_are_no_seeds():
    voronoi = ManhattanVoronoi(seeds=[])
    assert set(voronoi.seeds_that_extend_indefinetely()) == set()


def test_single_seed_extends_indefinetely():
    voronoi = ManhattanVoronoi(seeds=[Vector2D(0, 0)])
    assert set(voronoi.seeds_that_extend_indefinetely()) == {Vector2D(0, 0)}


def test_seeds_confined_by_others_do_not_grow_indefinetely():
    voronoi = ManhattanVoronoi(
        seeds=[
            Vector2D(1, 1),
            Vector2D(1, 6),
            Vector2D(8, 3),
            Vector2D(3, 4),
            Vector2D(5, 5),
            Vector2D(8, 9),
        ]
    )
    assert set(voronoi.seeds_that_extend_indefinetely()) == {
        Vector2D(1, 1),
        Vector2D(1, 6),
        Vector2D(8, 3),
        Vector2D(8, 9),
    }


def test_voronoi_seeds_grow_until_reaching_maximum_area():
    voronoi = ManhattanVoronoi(
        seeds=[
            Vector2D(1, 1),
            Vector2D(1, 6),
            Vector2D(8, 3),
            Vector2D(3, 4),
            Vector2D(5, 5),
            Vector2D(8, 9),
        ]
    )
    assert voronoi.areas_after_expansion() == {
        Vector2D(1, 1): inf,
        Vector2D(1, 6): inf,
        Vector2D(8, 3): inf,
        Vector2D(3, 4): 9,
        Vector2D(5, 5): 17,
        Vector2D(8, 9): inf,
    }
