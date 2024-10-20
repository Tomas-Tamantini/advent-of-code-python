from ..logic import Pulse, PulseType, PulseCounter


def test_pulse_counter_counts_high_and_low_pulses():
    counter = PulseCounter()
    counter.track(Pulse("a", "b", PulseType.HIGH))
    counter.track(Pulse("b", "c", PulseType.LOW))
    counter.track(Pulse("c", "d", PulseType.HIGH))
    assert counter.num_high_pulses == 2
    assert counter.num_low_pulses == 1
