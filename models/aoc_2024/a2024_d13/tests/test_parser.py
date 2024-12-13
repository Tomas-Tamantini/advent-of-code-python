from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..claw_machine import ClawMachine
from ..parser import parse_claw_machines


def test_parse_claw_machines():
    file_content = """
                   Button A: X+94, Y+34
                   Button B: X+22, Y+67
                   Prize: X=8400, Y=5400

                   Button A: X+26, Y+66
                   Button B: X+67, Y+21
                   Prize: X=12748, Y=12176"""

    input_reader = InputFromString(file_content)
    machines = list(parse_claw_machines(input_reader))
    assert machines == [
        ClawMachine(
            btn_a_offset=Vector2D(94, 34),
            btn_b_offset=Vector2D(22, 67),
            prize_location=Vector2D(8400, 5400),
        ),
        ClawMachine(
            btn_a_offset=Vector2D(26, 66),
            btn_b_offset=Vector2D(67, 21),
            prize_location=Vector2D(12748, 12176),
        ),
    ]
