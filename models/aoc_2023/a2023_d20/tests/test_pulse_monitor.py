from ..logic import LowPulseMonitor, Pulse, PulseCounter, PulseHistory, PulseType


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


def test_low_pulse_monitor_keeps_track_of_whether_all_monitored_modules_received_low_pulse():
    monitor = LowPulseMonitor(modules_to_monitor={"a", "b"})
    assert not monitor.all_monitored_modules_received_low_pulse()
    monitor.track(Pulse("x", "a", PulseType.HIGH))
    assert not monitor.all_monitored_modules_received_low_pulse()
    monitor.track(Pulse("x", "a", PulseType.LOW))
    assert not monitor.all_monitored_modules_received_low_pulse()
    monitor.track(Pulse("x", "a", PulseType.LOW))
    assert not monitor.all_monitored_modules_received_low_pulse()
    monitor.track(Pulse("x", "b", PulseType.HIGH))
    assert not monitor.all_monitored_modules_received_low_pulse()
    monitor.track(Pulse("x", "b", PulseType.LOW))
    assert monitor.all_monitored_modules_received_low_pulse()


def test_low_pulse_monitor_keeps_track_of_when_all_monitored_modules_received_low_pulse():
    monitor = LowPulseMonitor(modules_to_monitor={"a", "b"})
    monitor.track(Pulse("x", "a", PulseType.HIGH))
    monitor.increment_iteration()
    monitor.track(Pulse("x", "a", PulseType.LOW))
    monitor.increment_iteration()
    monitor.track(Pulse("x", "a", PulseType.LOW))
    monitor.track(Pulse("x", "b", PulseType.HIGH))
    monitor.increment_iteration()
    monitor.track(Pulse("x", "b", PulseType.LOW))
    assert monitor.num_iterations_until_first_low_pulse() == {"a": 1, "b": 3}
