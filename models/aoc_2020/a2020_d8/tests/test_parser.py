from models.common.io import InputFromString
from ..parser import parse_game_console_instructions
from ..logic import JumpOrNoOpInstruction, IncrementGlobalAccumulatorInstruction


def test_parse_game_console_instructions():
    file_content = """
                   nop +0
                   acc -1
                   jmp +4
                   """
    instructions = list(parse_game_console_instructions(InputFromString(file_content)))
    assert instructions == [
        JumpOrNoOpInstruction(offset=0, is_jump=False),
        IncrementGlobalAccumulatorInstruction(increment=-1),
        JumpOrNoOpInstruction(offset=4, is_jump=True),
    ]
