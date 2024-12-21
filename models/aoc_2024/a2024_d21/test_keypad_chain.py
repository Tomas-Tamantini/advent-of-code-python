import pytest

from .logic import CODE_ROBOT, DIRECTIONAL_ROBOT, min_num_keypad_presses


def test_min_num_keypad_presses_with_no_directional_robots():
    assert (
        min_num_keypad_presses(
            code="029A",
            code_robot=CODE_ROBOT,
            directional_robot=DIRECTIONAL_ROBOT,
            num_directional_robots=0,
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
            code_robot=CODE_ROBOT,
            directional_robot=DIRECTIONAL_ROBOT,
            num_directional_robots=2,
        )
        == expected
    )


def test_min_num_keypad_presses_is_calculated_efficiently():
    assert (
        min_num_keypad_presses(
            code="029A",
            code_robot=CODE_ROBOT,
            directional_robot=DIRECTIONAL_ROBOT,
            num_directional_robots=25,
        )
        == 82050061710
    )
