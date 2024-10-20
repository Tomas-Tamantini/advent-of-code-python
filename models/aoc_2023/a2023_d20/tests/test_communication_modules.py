from ..logic import Pulse, PulseType, FlipFlopModule


def _flip_flop(name="T", ouput_module_name="dest"):
    return FlipFlopModule(name, ouput_module_name)


def test_flip_flop_module_starts_off():
    module = _flip_flop()
    assert not module.is_on


def test_flip_flop_module_ignores_high_pulse():
    module = _flip_flop()
    input_pulse = Pulse("orig", "T", PulseType.HIGH)
    assert list(module.propagate(input_pulse)) == []


def test_flip_flop_module_flips_state_after_receiving_low_pulse():
    module = _flip_flop()
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    _ = list(module.propagate(input_pulse))
    assert module.is_on
    _ = list(module.propagate(input_pulse))
    assert not module.is_on


def test_flip_flop_sends_high_pulse_if_it_flipped_to_on():
    module = _flip_flop(ouput_module_name="dest")
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    output_pulses = list(module.propagate(input_pulse))
    assert output_pulses == [Pulse("T", "dest", PulseType.HIGH)]


def test_flip_flop_sends_low_pulse_if_it_flipped_to_off():
    module = _flip_flop(ouput_module_name="dest")
    input_pulse = Pulse("orig", "T", PulseType.LOW)
    _ = list(module.propagate(input_pulse))
    output_pulses = list(module.propagate(input_pulse))
    assert output_pulses == [Pulse("T", "dest", PulseType.LOW)]
