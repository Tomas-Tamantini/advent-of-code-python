from ..logic import RegisterHistory, InstructionWithDuration


def test_register_history_starts_with_value_one():
    rh = RegisterHistory()
    assert rh.value_during_cycle(1) == 1


def test_register_history_increments_value_after_instruction_duration():
    rh = RegisterHistory()
    rh.run_instruction(InstructionWithDuration(value_increment=123, num_cycles=3))
    assert rh.value_during_cycle(1) == 1
    assert rh.value_during_cycle(2) == 1
    assert rh.value_during_cycle(3) == 1
    assert rh.value_during_cycle(4) == 124


def test_register_history_keeps_last_value_forever_after():
    rh = RegisterHistory()
    rh.run_instruction(InstructionWithDuration(value_increment=123, num_cycles=3))
    assert rh.value_during_cycle(1_000_000) == 124


def test_register_history_runs_instructions_one_after_the_other():
    rh = RegisterHistory()
    rh.run_instruction(InstructionWithDuration(value_increment=123, num_cycles=3))
    rh.run_instruction(InstructionWithDuration(value_increment=456, num_cycles=2))
    assert rh.value_during_cycle(1) == 1
    assert rh.value_during_cycle(2) == 1
    assert rh.value_during_cycle(3) == 1
    assert rh.value_during_cycle(4) == 124
    assert rh.value_during_cycle(5) == 124
    assert rh.value_during_cycle(6) == 580
