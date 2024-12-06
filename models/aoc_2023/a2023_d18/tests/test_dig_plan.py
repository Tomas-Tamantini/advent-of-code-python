from models.common.vectors import CardinalDirection, Vector2D

from ..dig_plan import DiggerInstruction, DigPlan


def test_digger_instruction_moves_digger_position():
    instruction = DiggerInstruction(CardinalDirection.EAST, 5)
    assert instruction.move(Vector2D(0, 0)) == Vector2D(5, 0)


def test_dig_plan_yields_dig_area():
    instructions = [
        DiggerInstruction(CardinalDirection.EAST, 6),
        DiggerInstruction(CardinalDirection.SOUTH, 5),
        DiggerInstruction(CardinalDirection.WEST, 2),
        DiggerInstruction(CardinalDirection.SOUTH, 2),
        DiggerInstruction(CardinalDirection.EAST, 2),
        DiggerInstruction(CardinalDirection.SOUTH, 2),
        DiggerInstruction(CardinalDirection.WEST, 5),
        DiggerInstruction(CardinalDirection.NORTH, 2),
        DiggerInstruction(CardinalDirection.WEST, 1),
        DiggerInstruction(CardinalDirection.NORTH, 2),
        DiggerInstruction(CardinalDirection.EAST, 2),
        DiggerInstruction(CardinalDirection.NORTH, 3),
        DiggerInstruction(CardinalDirection.WEST, 2),
        DiggerInstruction(CardinalDirection.NORTH, 2),
    ]
    dig_plan = DigPlan(instructions)
    assert dig_plan.dig_area() == 62
