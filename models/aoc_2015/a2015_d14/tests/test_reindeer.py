from ..reindeer import Reindeer, ReindeerOlympics

comet = Reindeer(flight_speed=14, flight_interval=10, rest_interval=127)
dancer = Reindeer(flight_speed=16, flight_interval=11, rest_interval=162)


def test_reindeer_starts_at_position_zero():
    assert comet.position_at_time(0) == 0


def test_reindeer_flies_at_constant_speed():
    assert comet.position_at_time(10) == 140


def test_reindeer_must_rest_after_maximum_flight_interval():
    assert comet.position_at_time(12) == 140


def test_reindeer_alternates_flight_and_rest():
    assert comet.position_at_time(1000) == 1120


def test_racing_reindeers_have_their_positions_tracked():
    reindeers = [comet, dancer]
    olympics = ReindeerOlympics(reindeers)
    assert olympics.positions_at_time(1000) == [1120, 1056]


def test_racing_reindeers_get_awarded_one_point_for_each_second_in_the_lead():
    reindeers = [comet, dancer]
    olympics = ReindeerOlympics(reindeers)
    assert olympics.points_at_time(1000) == [312, 689]
