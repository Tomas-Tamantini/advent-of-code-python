import pytest

from .logic import (
    DIRECTIONAL_ROBOT,
    NUMERIC_ROBOT,
    KeypadRobots,
    min_num_keypad_presses,
)


def _directional_robots(num_robots: int) -> KeypadRobots:
    return KeypadRobots(DIRECTIONAL_ROBOT, num_robots)


def test_min_num_keypad_presses_with_no_directional_robots():
    assert (
        min_num_keypad_presses(
            code="029A",
            numeric_robot=NUMERIC_ROBOT,
            directional_robots=_directional_robots(num_robots=0),
        )
        == 12
    )


@pytest.mark.parametrize(
    ("code", "expected"),
    [("029A", 68), ("980A", 60), ("179A", 68), ("456A", 64), ("379A", 64)],
)
def test_min_num_keypad_presses_with_two_directional_robots(code, expected):
    assert (
        min_num_keypad_presses(
            code,
            numeric_robot=NUMERIC_ROBOT,
            directional_robots=_directional_robots(num_robots=2),
        )
        == expected
    )


def test_min_num_keypad_presses_is_calculated_efficiently():
    assert (
        min_num_keypad_presses(
            code="029A",
            numeric_robot=NUMERIC_ROBOT,
            directional_robots=_directional_robots(num_robots=25),
        )
        == 82050061710
    )
