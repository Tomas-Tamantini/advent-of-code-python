import pytest

from ..logic import AndGate, OrGate, Pulse, PulseType, XorGate


def _parse_pulse_level(level: int) -> PulseType:
    return PulseType.HIGH if level == 1 else PulseType.LOW


@pytest.mark.parametrize(
    ("in_a", "in_b", "out"),
    [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 1)],
)
def test_and_gate_returns_high_if_both_inputs_are_high(in_a, in_b, out):
    gate = AndGate("x", "y", "z")
    output = gate.output(
        signal_a=_parse_pulse_level(in_a), signal_b=_parse_pulse_level(in_b)
    )
    assert Pulse("z", _parse_pulse_level(out)) == output


@pytest.mark.parametrize(
    ("in_a", "in_b", "out"),
    [(0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)],
)
def test_or_gate_returns_high_if_some_input_is_high(in_a, in_b, out):
    gate = OrGate("x", "y", "z")
    output = gate.output(
        signal_a=_parse_pulse_level(in_a), signal_b=_parse_pulse_level(in_b)
    )
    assert Pulse("z", _parse_pulse_level(out)) == output


@pytest.mark.parametrize(
    ("in_a", "in_b", "out"),
    [(0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0)],
)
def test_xor_gate_returns_high_if_only_one_input_is_high(in_a, in_b, out):
    gate = XorGate("x", "y", "z")
    output = gate.output(
        signal_a=_parse_pulse_level(in_a), signal_b=_parse_pulse_level(in_b)
    )
    assert Pulse("z", _parse_pulse_level(out)) == output
