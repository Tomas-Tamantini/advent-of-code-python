from models.aoc_2015 import Reindeer

reindeer = Reindeer(flight_speed=14, flight_interval=10, rest_interval=127)


def test_reindeer_starts_at_position_zero():
    assert reindeer.position_at_time(0) == 0


def test_reindeer_flies_at_constant_speed():
    assert reindeer.position_at_time(10) == 140


def test_reindeer_must_rest_after_maximum_flight_interval():
    assert reindeer.position_at_time(12) == 140


def test_reindeer_alternates_flight_and_rest():
    assert reindeer.position_at_time(1000) == 1120
