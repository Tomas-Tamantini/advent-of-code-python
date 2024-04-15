from unittest.mock import Mock
from models.aoc_2020 import (
    IncrementGlobalAccumulatorInstruction,
    UnconditionalJumpInstruction,
)


def test_unconditional_jump_instruction_updates_program_counter():
    instruction = UnconditionalJumpInstruction(2)
    hardware = Mock()
    instruction.execute(hardware)
    hardware.increment_program_counter.assert_called_once_with(2)


def test_increment_global_accumulator_updates_accumulator():
    instruction = IncrementGlobalAccumulatorInstruction(3)
    hardware = Mock()
    hardware.global_accumulator = 0
    instruction.execute(hardware)
    assert hardware.global_accumulator == 3
