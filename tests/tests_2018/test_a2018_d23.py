from models.vectors import Vector3D
from models.aoc_2018 import TeleportNanobot, distance_of_position_with_strongest_signal


def test_position_with_manhattan_distance_larger_than_radius_is_not_in_range_of_nanobot():
    nanobot = TeleportNanobot(radius=3, position=Vector3D(0, 0, 0))
    assert not nanobot.is_in_range(Vector3D(4, 0, 0))


def test_position_within_manhattan_distance_equal_to_radius_is_in_range_of_nanobot():
    nanobot = TeleportNanobot(radius=3, position=Vector3D(0, 0, 0))
    assert nanobot.is_in_range(Vector3D(1, -1, 1))


def test_position_with_strongest_signal_if_not_bots_is_origin():
    assert distance_of_position_with_strongest_signal(nanobots=[]) == 0


def test_position_with_strongest_signal_with_single_nanobot_is_point_in_range_closest_to_origin():
    nanobot = TeleportNanobot(radius=3, position=Vector3D(20, 0, 0))
    assert distance_of_position_with_strongest_signal(nanobots=[nanobot]) == 17
