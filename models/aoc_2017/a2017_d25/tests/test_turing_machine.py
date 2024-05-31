from ..turing_machine import TuringMachine, TuringState, TuringRule


def test_turing_machine_starts_with_all_zeroes_on_tape():
    machine = TuringMachine()
    assert machine.sum_tape_values == 0


def test_turing_machine_can_run_arbitrary_program():
    machine = TuringMachine()
    transition_rules = {
        TuringState("A", 0): TuringRule("B", write_value=1, move=1),
        TuringState("A", 1): TuringRule("B", write_value=0, move=-1),
        TuringState("B", 0): TuringRule("A", write_value=1, move=-1),
        TuringState("B", 1): TuringRule("A", write_value=1, move=1),
    }
    initial_state = "A"
    steps = 6
    machine.run(transition_rules, initial_state, steps)
    assert machine.sum_tape_values == 3
