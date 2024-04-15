import pytest
from unittest.mock import Mock
from models.assembly import NoOpInstruction
from models.aoc_2020 import (
    IncrementGlobalAccumulatorInstruction,
    UnconditionalJumpInstruction,
    GameConsoleProgram,
    run_game_console,
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


def test_increment_global_accumulator_increments_program_counter_by_one():
    instruction = IncrementGlobalAccumulatorInstruction(3)
    hardware = Mock()
    hardware.global_accumulator = 0
    instruction.execute(hardware)
    hardware.increment_program_counter.assert_called_once_with(1)


def test_game_console_program_fetches_instruction_from_program_counter():
    acc = IncrementGlobalAccumulatorInstruction(1)
    jmp = UnconditionalJumpInstruction(2)
    program = GameConsoleProgram(instructions=[acc, jmp])
    instruction = program.get_instruction(1)
    assert instruction == jmp
    instruction = program.get_instruction(0)
    assert instruction == acc


def test_game_console_program_raises_index_error_if_fetching_instruction_outside_range():
    program = GameConsoleProgram(
        instructions=[
            IncrementGlobalAccumulatorInstruction(1),
            UnconditionalJumpInstruction(2),
        ]
    )
    with pytest.raises(IndexError):
        program.get_instruction(2)

    with pytest.raises(IndexError):
        program.get_instruction(-1)


def test_game_console_program_raises_repeated_instruction_error_if_fetching_same_instruction_twice():
    program = GameConsoleProgram(
        instructions=[
            IncrementGlobalAccumulatorInstruction(1),
            UnconditionalJumpInstruction(2),
        ]
    )
    program.get_instruction(0)
    program.get_instruction(1)
    with pytest.raises(GameConsoleProgram.RepeatedInstructionError):
        program.get_instruction(0)


def test_game_console_program_until_first_repeated_line_and_returns_global_accumulator():
    instructions = [
        NoOpInstruction(),
        IncrementGlobalAccumulatorInstruction(1),
        UnconditionalJumpInstruction(4),
        IncrementGlobalAccumulatorInstruction(3),
        UnconditionalJumpInstruction(-3),
        IncrementGlobalAccumulatorInstruction(-99),
        IncrementGlobalAccumulatorInstruction(1),
        UnconditionalJumpInstruction(-4),
        IncrementGlobalAccumulatorInstruction(6),
    ]
    accumulator = run_game_console(instructions)
    assert accumulator == 5
