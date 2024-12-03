from ..logic import (
    MultiplicationInstruction,
    DoInstruction,
    DontInstruction,
    StackWithoutConditional,
    StackWithConditional,
)

_INSTRUCTIONS = [
    MultiplicationInstruction(2, 4),
    DontInstruction(),
    MultiplicationInstruction(5, 5),
    MultiplicationInstruction(11, 8),
    DoInstruction(),
    MultiplicationInstruction(8, 5),
]


def test_stack_without_conditional_ignores_dos_and_donts_instructions():
    stack = StackWithoutConditional()
    for instruction in _INSTRUCTIONS:
        instruction.execute(stack)
    assert stack.result == 161


def test_stack_with_conditional_applies_dos_and_donts_instructions():
    stack = StackWithConditional()
    for instruction in _INSTRUCTIONS:
        instruction.execute(stack)
    assert stack.result == 48
