from models.aoc_2018 import TeleportNanobot


def test_position_with_manhattan_distance_larger_than_radius_is_not_in_range_of_nanobot():
    nanobot = TeleportNanobot(radius=3, position=(0, 0, 0))
    assert not nanobot.is_in_range((4, 0, 0))


def test_position_within_manhattan_distance_equal_to_radius_is_in_range_of_nanobot():
    nanobot = TeleportNanobot(radius=3, position=(0, 0, 0))
    assert nanobot.is_in_range((1, -1, 1))
