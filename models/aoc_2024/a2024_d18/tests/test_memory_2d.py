from models.common.vectors import Vector2D

from ..memory_2d import Memory2D


def test_shortest_path_through_uncorrupted_memory_is_manhattan_distance():
    memory = Memory2D(width=5, height=5, corrupted_positions=[])
    assert memory.shortest_path(Vector2D(0, 0), Vector2D(4, 4)) == 8


def test_shortest_path_through_corrupted_memory_avoids_corrupted_positions():
    corrupted_positions = [
        Vector2D(5, 4),
        Vector2D(4, 2),
        Vector2D(4, 5),
        Vector2D(3, 0),
        Vector2D(2, 1),
        Vector2D(6, 3),
        Vector2D(2, 4),
        Vector2D(1, 5),
        Vector2D(0, 6),
        Vector2D(3, 3),
        Vector2D(2, 6),
        Vector2D(5, 1),
    ]
    memory = Memory2D(7, 7, corrupted_positions)
    assert memory.shortest_path(Vector2D(0, 0), Vector2D(6, 6)) == 22
