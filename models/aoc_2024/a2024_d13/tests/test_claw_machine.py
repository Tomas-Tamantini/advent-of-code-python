import pytest

from models.common.vectors import Vector2D

from ..claw_machine import ClawMachine

_machine_a = ClawMachine(
    btn_a_offset=Vector2D(94, 34),
    btn_b_offset=Vector2D(22, 67),
    prize_location=Vector2D(8400, 5400),
)

_machine_b = ClawMachine(
    btn_a_offset=Vector2D(26, 66),
    btn_b_offset=Vector2D(67, 21),
    prize_location=Vector2D(12748, 12176),
)

_machine_c = ClawMachine(
    btn_a_offset=Vector2D(17, 86),
    btn_b_offset=Vector2D(84, 37),
    prize_location=Vector2D(7870, 6450),
)

_machine_d = ClawMachine(
    btn_a_offset=Vector2D(69, 23),
    btn_b_offset=Vector2D(27, 71),
    prize_location=Vector2D(18641, 10279),
)

_machine_e = ClawMachine(
    btn_a_offset=Vector2D(1, 0),
    btn_b_offset=Vector2D(0, 1),
    prize_location=Vector2D(101, 0),
)

_machine_f = ClawMachine(
    btn_a_offset=Vector2D(1, 0),
    btn_b_offset=Vector2D(0, 1),
    prize_location=Vector2D(0, 101),
)


@pytest.mark.parametrize(
    ("machine", "expected"), [(_machine_a, (80, 40)), (_machine_c, (38, 86))]
)
def test_claw_machine_calculates_number_of_button_pushes_to_get_prize(
    machine: ClawMachine, expected: tuple[int, int]
):
    num_presses = machine.num_button_presses_to_get_prize()
    assert expected == num_presses


@pytest.mark.parametrize("machine", [_machine_b, _machine_d])
def test_claw_machine_returns_none_if_impossible_to_get_prize(machine: ClawMachine):
    num_presses = machine.num_button_presses_to_get_prize()
    assert num_presses is None


@pytest.mark.parametrize("machine", [_machine_e, _machine_f])
def test_claw_machine_returns_none_if_requires_more_than_100_button_presses_for_some_button(
    machine: ClawMachine,
):
    num_presses = machine.num_button_presses_to_get_prize()
    assert num_presses is None
