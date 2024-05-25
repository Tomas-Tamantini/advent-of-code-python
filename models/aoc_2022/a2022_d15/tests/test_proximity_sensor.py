from models.common.vectors import Vector2D
from models.common.number_theory import Interval
from ..logic import ProximitySensor


def _example_sensor() -> ProximitySensor:
    return ProximitySensor(
        position=Vector2D(8, 7),
        nearest_beacon=Vector2D(2, 10),
    )


def test_interval_which_cannot_be_beacon_is_none_in_row_farther_than_nearest_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=17) is None


def test_interval_which_cannot_be_beacon_is_calculated_properly_in_row_closer_than_nearest_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=9) == Interval(1, 15)


def test_interval_which_cannot_be_beacon_discounts_existing_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=10) == Interval(3, 14)
