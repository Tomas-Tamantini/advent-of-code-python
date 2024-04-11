from models.aoc_2019.a2019_d21 import (
    SpringScriptInstruction,
    SpringScriptInstructionType,
)


def test_springscript_instruction_can_be_converted_to_string():
    instruction = SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "B")
    assert str(instruction) == "AND A B"
