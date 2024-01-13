import pytest
from models.cellular_automata import ElementaryAutomaton


def test_rule_index_must_be_between_0_and_255():
    with pytest.raises(ValueError):
        _ = ElementaryAutomaton(rule=-1)

    with pytest.raises(ValueError):
        _ = ElementaryAutomaton(rule=256)


def test_rule_zero_switches_off_all_cells():
    automaton = ElementaryAutomaton(rule=0)
    current_state = "11111"
    assert automaton.next_state(current_state) == "00000"


def test_rule_110_produces_A117999_OEIS_sequence():
    automaton = ElementaryAutomaton(rule=110)
    expected_states = [
        "000010000",
        "000110000",
        "001110000",
        "011010000",
        "111110000",
    ]
    for i in range(1, len(expected_states)):
        assert automaton.next_state(expected_states[i - 1]) == expected_states[i]
