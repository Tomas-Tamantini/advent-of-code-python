from ..logic import Pulse, PulseType, BroadcastModule, FlipFlopModule


def test_broadcast_module_sends_signal_forward():
    module = BroadcastModule("M")
    high_pulse = Pulse("orig", "M", PulseType.HIGH)
    assert module.propagate(high_pulse) == PulseType.HIGH
    low_pulse = Pulse("orig", "M", PulseType.LOW)
    assert module.propagate(low_pulse) == PulseType.LOW


def test_flip_flop_module_starts_off():
    module = FlipFlopModule("F")
    assert not module.is_on


def test_flip_flop_module_ignores_high_pulse():
    module = FlipFlopModule("F")
    input_pulse = Pulse("orig", "T", PulseType.HIGH)
    assert module.propagate(input_pulse) is None


def test_flip_flop_module_flips_state_after_receiving_low_pulse():
    module = FlipFlopModule("F")
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    module.propagate(input_pulse)
    assert module.is_on
    module.propagate(input_pulse)
    assert not module.is_on


def test_flip_flop_sends_high_pulse_if_it_flipped_to_on():
    module = FlipFlopModule("F")
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    assert module.propagate(input_pulse) == PulseType.HIGH


def test_flip_flop_sends_low_pulse_if_it_flipped_to_off():
    module = FlipFlopModule("F")
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    module.propagate(input_pulse)
    assert module.propagate(input_pulse) == PulseType.LOW
