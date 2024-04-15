import pytest
from unittest.mock import Mock
from models.aoc_2020 import (
    IncrementGlobalAccumulatorInstruction,
    JumpOrNoOpInstruction,
    GameConsoleProgram,
    run_game_console,
    find_and_run_game_console_which_terminates,
)


def test_jump_or_noop_instruction_increments_program_counter_by_offset_if_jump():
    instruction = JumpOrNoOpInstruction(offset=2, is_jump=True)
    hardware = Mock()
    instruction.execute(hardware)
    hardware.increment_program_counter.assert_called_once_with(2)


def test_jump_or_noop_instruction_increments_program_counter_by_one_if_not_jump():
    instruction = JumpOrNoOpInstruction(offset=2, is_jump=False)
    hardware = Mock()
    instruction.execute(hardware)
    hardware.increment_program_counter.assert_called_once_with(1)


def test_jump_or_noop_instruction_can_toggle_between_the_two():
    jump = JumpOrNoOpInstruction(offset=2, is_jump=True)
    noop = JumpOrNoOpInstruction(offset=2, is_jump=False)
    assert jump.toggle() == noop
    assert noop.toggle() == jump


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
    jmp = JumpOrNoOpInstruction(2, is_jump=True)
    program = GameConsoleProgram(instructions=[acc, jmp])
    instruction = program.get_instruction(1)
    assert instruction == jmp
    instruction = program.get_instruction(0)
    assert instruction == acc


def test_game_console_program_returns_none_if_fetching_instruction_outside_range():
    program = GameConsoleProgram(
        instructions=[
            IncrementGlobalAccumulatorInstruction(1),
            JumpOrNoOpInstruction(2),
        ]
    )
    assert program.get_instruction(2) is None
    assert program.get_instruction(-1) is None


def test_game_console_program_raises_repeated_instruction_error_if_fetching_same_instruction_twice():
    program = GameConsoleProgram(
        instructions=[
            IncrementGlobalAccumulatorInstruction(1),
            JumpOrNoOpInstruction(2),
        ]
    )
    program.get_instruction(0)
    program.get_instruction(1)
    with pytest.raises(GameConsoleProgram.RepeatedInstructionError):
        program.get_instruction(0)


def test_game_console_program_returns_toggled_instruction_at_given_index():
    program = GameConsoleProgram(
        instructions=[
            IncrementGlobalAccumulatorInstruction(1),
            JumpOrNoOpInstruction(2),
        ],
        index_to_toggle=1,
    )
    instruction = program.get_instruction(1)
    assert instruction == JumpOrNoOpInstruction(2, is_jump=False)


def test_game_console_program_raises_index_error_if_index_to_toggle_is_not_jump_or_noop_instruction():
    with pytest.raises(IndexError):
        _ = GameConsoleProgram(
            instructions=[
                IncrementGlobalAccumulatorInstruction(1),
                JumpOrNoOpInstruction(2),
            ],
            index_to_toggle=0,
        )


def test_game_console_program_until_first_repeated_line_and_returns_global_accumulator():
    instructions = [
        JumpOrNoOpInstruction(0, is_jump=False),
        IncrementGlobalAccumulatorInstruction(1),
        JumpOrNoOpInstruction(4),
        IncrementGlobalAccumulatorInstruction(3),
        JumpOrNoOpInstruction(-3),
        IncrementGlobalAccumulatorInstruction(-99),
        IncrementGlobalAccumulatorInstruction(1),
        JumpOrNoOpInstruction(-4),
        IncrementGlobalAccumulatorInstruction(6),
    ]
    accumulator = run_game_console(instructions)
    assert accumulator == 5


def test_game_console_toggles_instructions_until_finding_one_which_makes_program_terminate():
    instructions = [
        JumpOrNoOpInstruction(0, is_jump=False),
        IncrementGlobalAccumulatorInstruction(1),
        JumpOrNoOpInstruction(4),
        IncrementGlobalAccumulatorInstruction(3),
        JumpOrNoOpInstruction(-3),
        IncrementGlobalAccumulatorInstruction(-99),
        IncrementGlobalAccumulatorInstruction(1),
        JumpOrNoOpInstruction(-4),
        IncrementGlobalAccumulatorInstruction(6),
    ]
    accumulator = find_and_run_game_console_which_terminates(instructions)
    assert accumulator == 8
