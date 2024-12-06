from models.common.io import InputFromString

from ..logic import InstructionWithDuration
from ..parser import parse_instructions_with_duration


def test_parse_instructions_with_duration():
    input_reader = InputFromString(
        """
        noop
        addx 3
        addx -5
        """
    )
    instructions = list(parse_instructions_with_duration(input_reader))
    assert instructions == [
        InstructionWithDuration(value_increment=0, num_cycles=1),
        InstructionWithDuration(value_increment=3, num_cycles=2),
        InstructionWithDuration(value_increment=-5, num_cycles=2),
    ]
