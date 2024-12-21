import pytest

from .logic import DIRECTIONAL_ROBOT, NUMERIC_ROBOT, KeypadChain


def test_min_num_keypad_presses_with_no_directional_robots():
    chain = KeypadChain(
        numeric_robot=NUMERIC_ROBOT,
        directional_robot=DIRECTIONAL_ROBOT,
        num_directional_robots=0,
    )
    assert chain.min_num_keypad_presses(code="029A") == 12


@pytest.mark.parametrize(
    ("code", "expected"),
    [("029A", 68), ("980A", 60), ("179A", 68), ("456A", 64), ("379A", 64)],
)
def test_min_num_keypad_presses_with_two_directional_robots(code, expected):
    chain = KeypadChain(
        numeric_robot=NUMERIC_ROBOT,
        directional_robot=DIRECTIONAL_ROBOT,
        num_directional_robots=2,
    )
    assert chain.min_num_keypad_presses(code) == expected


def test_min_num_keypad_presses_is_calculated_efficiently():
    chain = KeypadChain(
        numeric_robot=NUMERIC_ROBOT,
        directional_robot=DIRECTIONAL_ROBOT,
        num_directional_robots=25,
    )
    assert chain.min_num_keypad_presses(code="029A") == 82050061710
