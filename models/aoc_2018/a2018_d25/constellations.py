from typing import Iterator

from models.common.graphs import DisjointSet


def _manhattan_distance(
    p1: tuple[int, int, int, int], p2: tuple[int, int, int, int]
) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))


def _valid_edges(
    max_distance: int, points: list[tuple[int, int, int, int]]
) -> Iterator[tuple[int, int]]:
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if _manhattan_distance(points[i], points[j]) <= max_distance:
                yield i, j


def num_constellations(
    max_distance: int, points: list[tuple[int, int, int, int]]
) -> int:
    constellations = DisjointSet()
    for point in points:
        constellations.make_set(point)
    for i, j in _valid_edges(max_distance, points):
        constellations.union(points[i], points[j])
    return constellations.num_sets
