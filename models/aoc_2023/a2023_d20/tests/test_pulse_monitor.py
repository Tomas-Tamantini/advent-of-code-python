from ..logic import Pulse, PulseType, PulseCounter, PulseHistory


def test_pulse_counter_counts_high_and_low_pulses():
    monitor = PulseCounter()
    monitor.track(Pulse("a", "b", PulseType.HIGH))
    monitor.track(Pulse("b", "c", PulseType.LOW))
    monitor.track(Pulse("c", "d", PulseType.HIGH))
    assert monitor.num_high_pulses == 2
    assert monitor.num_low_pulses == 1


def test_pulse_history_monitor_saves_every_pulse():
    monitor = PulseHistory()
    monitor.track(Pulse("a", "b", PulseType.HIGH))
    monitor.track(Pulse("b", "c", PulseType.LOW))
    assert list(monitor.history()) == [
        Pulse("a", "b", PulseType.HIGH),
        Pulse("b", "c", PulseType.LOW),
    ]
