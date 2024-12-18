from models.common.vectors import Vector2D

from ..memory_2d import Memory2D, index_of_first_blocking_byte


def test_shortest_path_through_uncorrupted_memory_is_manhattan_distance():
    memory = Memory2D(width=5, height=5, corrupted_positions=[])
    assert memory.shortest_path(Vector2D(0, 0), Vector2D(4, 4)) == 8


_corrupted_positions = [
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
    Vector2D(1, 2),
    Vector2D(5, 5),
    Vector2D(2, 5),
    Vector2D(6, 5),
    Vector2D(1, 4),
    Vector2D(0, 4),
    Vector2D(6, 4),
    Vector2D(1, 1),
    Vector2D(6, 1),
    Vector2D(1, 0),
    Vector2D(0, 5),
    Vector2D(1, 6),
    Vector2D(2, 0),
]


def test_shortest_path_through_corrupted_memory_avoids_corrupted_positions():
    memory = Memory2D(7, 7, _corrupted_positions[:12])
    assert memory.shortest_path(Vector2D(0, 0), Vector2D(6, 6)) == 22


def test_shortest_path_through_corrupted_memory_is_minus_one_if_no_possible_path():
    corrupted_positions = [Vector2D(0, 1), Vector2D(1, 0)]
    memory = Memory2D(2, 2, corrupted_positions)
    assert memory.shortest_path(Vector2D(0, 0), Vector2D(1, 1)) == -1


def test_can_find_index_of_first_blocking_byte():
    memory_size = (7, 7)
    assert index_of_first_blocking_byte(memory_size, _corrupted_positions) == 20
