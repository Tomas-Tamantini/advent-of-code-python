from models.common.io import InputFromString
from ..parser import parse_turing_machine_specs
from ..turing_machine import TuringState, TuringRule


def test_parse_turing_machine_specs():
    file_content = """Begin in state A.
                      Perform a diagnostic checksum after 6 steps.
 
                      In state A:
                      If the current value is 0:
                          - Write the value 1.
                          - Move one slot to the right.
                          - Continue with state B.
                      If the current value is 1:
                          - Write the value 0.
                          - Move one slot to the left.
                          - Continue with state B.

                      In state B:
                      If the current value is 0:
                          - Write the value 1.
                          - Move one slot to the left.
                          - Continue with state A.
                      If the current value is 1:
                          - Write the value 1.
                          - Move one slot to the right.
                          - Continue with state A."""
    initial_state, num_steps, transition_rules = parse_turing_machine_specs(
        InputFromString(file_content)
    )
    assert initial_state == "A"
    assert num_steps == 6
    assert transition_rules == {
        TuringState("A", 0): TuringRule("B", write_value=1, move=1),
        TuringState("A", 1): TuringRule("B", write_value=0, move=-1),
        TuringState("B", 0): TuringRule("A", write_value=1, move=-1),
        TuringState("B", 1): TuringRule("A", write_value=1, move=1),
    }
