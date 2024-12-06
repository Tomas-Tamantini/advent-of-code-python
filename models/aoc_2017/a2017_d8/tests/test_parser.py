from models.common.io import InputFromString

from ..conditional_increment import ComparisonOperator, ConditionalIncrementInstruction
from ..parser import parse_conditional_increment_instructions


def test_parse_conditional_increment_instructions():
    file_content = """b inc 5 if a > 1
                      a inc 1 if b < 5
                      c dec -10 if a >= 1
                      c inc -20 if c == 10"""
    instructions = list(
        parse_conditional_increment_instructions(InputFromString(file_content))
    )
    assert instructions[0] == ConditionalIncrementInstruction(
        "b", 5, "a", 1, ComparisonOperator.GREATER_THAN
    )
    assert instructions[1] == ConditionalIncrementInstruction(
        "a", 1, "b", 5, ComparisonOperator.LESS_THAN
    )
    assert instructions[2] == ConditionalIncrementInstruction(
        "c", 10, "a", 1, ComparisonOperator.GREATER_THAN_OR_EQUAL
    )
    assert instructions[3] == ConditionalIncrementInstruction(
        "c", -20, "c", 10, ComparisonOperator.EQUALS
    )
