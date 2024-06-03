import pytest
from models.common.io import InputFromString
from ..parser import parse_bitmask_instructions
from ..bitmask_memory import SetMaskInstruction, WriteToMemoryInstruction


@pytest.mark.parametrize("is_address_mask", [True, False])
def test_parse_bitmask_instructions_for_values(is_address_mask):
    file_content = """
                   mask = XXX
                   mem[8] = 123
                   mask = 1X0
                   mem[7] = 456
                   """
    instructions = list(
        parse_bitmask_instructions(InputFromString(file_content), is_address_mask)
    )
    assert instructions == [
        SetMaskInstruction("XXX", is_address_mask),
        WriteToMemoryInstruction(address=8, value=123),
        SetMaskInstruction("1X0", is_address_mask),
        WriteToMemoryInstruction(address=7, value=456),
    ]
