from ..logic import Pulse, PulseType, BroadcastModule, FlipFlopModule, ConjunctionModule


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


def test_resetting_flip_flop_module_flips_it_to_off():
    module = FlipFlopModule("F")
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    module.propagate(input_pulse)
    module.reset()
    assert not module.is_on


def test_conjuction_module_starts_with_all_inputs_low():
    module = ConjunctionModule("C", num_inputs=3)
    assert module.num_high_inputs == 0


def test_conjuction_module_remembers_how_many_inputs_are_high():
    module = ConjunctionModule("C", num_inputs=3)
    module.propagate(Pulse("in1", "C", PulseType.LOW))
    module.propagate(Pulse("in2", "C", PulseType.HIGH))
    module.propagate(Pulse("in3", "C", PulseType.HIGH))
    module.propagate(Pulse("in2", "C", PulseType.LOW))
    module.propagate(Pulse("in1", "C", PulseType.HIGH))
    assert module.num_high_inputs == 2  # in1 and in3


def test_conjuction_module_sends_low_pulse_if_all_inputs_are_high_otherwise_sends_low():
    module = ConjunctionModule("C", num_inputs=3)
    assert module.propagate(Pulse("in1", "C", PulseType.HIGH)) == PulseType.HIGH
    assert module.propagate(Pulse("in2", "C", PulseType.HIGH)) == PulseType.HIGH
    assert module.propagate(Pulse("in3", "C", PulseType.HIGH)) == PulseType.LOW
    assert module.propagate(Pulse("in2", "C", PulseType.LOW)) == PulseType.HIGH
    assert module.propagate(Pulse("in2", "C", PulseType.HIGH)) == PulseType.LOW


def test_restting_conjuction_module_sets_all_inputs_to_low():
    module = ConjunctionModule("C", num_inputs=3)
    module.propagate(Pulse("in1", "C", PulseType.HIGH))
    module.reset()
    assert module.num_high_inputs == 0
