from .constellations import num_constellations


def test_num_constellations_for_zero_points_is_zero():
    assert num_constellations(max_distance=3, points=[]) == 0


def test_num_constellations_for_one_point_is_one():
    assert num_constellations(max_distance=3, points=[(1, 2, 3, 4)]) == 1


def test_each_point_is_constellation_if_they_are_far_apart():
    points_far_apart = [(1, 2, 3, 4), (10, 20, 30, 40), (-1000, 0, 0, 0)]
    assert num_constellations(max_distance=3, points=points_far_apart) == 3


def test_points_close_together_join_into_single_constellation():
    points = [
        (0, 0, 0, 0),
        (3, 0, 0, 0),
        (0, 3, 0, 0),
        (0, 0, 3, 0),
        (0, 0, 0, 3),
        (0, 0, 0, 6),
        (9, 0, 0, 0),
        (12, 0, 0, 0),
    ]
    assert num_constellations(max_distance=3, points=points) == 2
