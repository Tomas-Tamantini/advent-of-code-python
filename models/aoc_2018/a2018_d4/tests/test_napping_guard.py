from datetime import datetime
from ..napping_guard import GuardNap, Guard


def test_guard_keeps_track_of_total_time_asleep():
    guard = Guard(
        id=0,
        naps=[
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 0),
                end_exclusive=datetime(1518, 11, 1, 0, 5),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 33),
                end_exclusive=datetime(1518, 11, 1, 0, 34),
            ),
        ],
    )

    assert guard.total_minutes_asleep == 6


def test_guard_keeps_track_of_minute_they_are_most_likely_to_be_asleep():
    guard = Guard(
        id=0,
        naps=[
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 5),
                end_exclusive=datetime(1518, 11, 1, 0, 25),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 30),
                end_exclusive=datetime(1518, 11, 1, 0, 55),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 3, 0, 24),
                end_exclusive=datetime(1518, 11, 3, 0, 29),
            ),
        ],
    )

    assert guard.minute_most_likely_to_be_asleep() == 24


def test_guard_keeps_track_of_how_many_times_they_slept_on_any_given_minute():
    guard = Guard(
        id=0,
        naps=[
            GuardNap(
                start_inclusive=datetime(1518, 11, 2, 0, 40),
                end_exclusive=datetime(1518, 11, 2, 0, 50),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 4, 0, 36),
                end_exclusive=datetime(1518, 11, 4, 0, 46),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 5, 0, 45),
                end_exclusive=datetime(1518, 11, 5, 0, 55),
            ),
        ],
    )

    assert guard.num_times_slept_on_minute(45) == 3
