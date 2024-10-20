from ..logic import (
    BroadcastModule,
    FlipFlopModule,
    ConjunctionModule,
    ModuleNetwork,
    Pulse,
    PulseType,
    PulseHistory,
)


def _example_network_1():
    modules = [
        BroadcastModule("broadcaster"),
        FlipFlopModule("a"),
        FlipFlopModule("b"),
        FlipFlopModule("c"),
        ConjunctionModule("inv", num_inputs=1),
    ]
    connections = {
        "broadcaster": ("a", "b", "c"),
        "a": ("b",),
        "b": ("c",),
        "c": ("inv",),
        "inv": ("a",),
    }
    return ModuleNetwork(modules, connections)


def _example_network_2():
    modules = [
        BroadcastModule("broadcaster"),
        FlipFlopModule("a"),
        FlipFlopModule("b"),
        ConjunctionModule("inv", num_inputs=1),
        ConjunctionModule("con", num_inputs=2),
    ]
    connections = {
        "broadcaster": ("a",),
        "a": ("inv", "con"),
        "b": ("con",),
        "inv": ("b",),
        "con": ("output",),
    }
    return ModuleNetwork(modules, connections)


def test_module_network_propagates_pulses_in_queue_order():
    network = _example_network_1()
    monitor = PulseHistory()
    initial_pulse = Pulse("button", "broadcaster", PulseType.LOW)
    network.propagate(initial_pulse, monitor)
    pulses = list(monitor.history())
    assert pulses == [
        Pulse("button", "broadcaster", PulseType.LOW),
        Pulse("broadcaster", "a", PulseType.LOW),
        Pulse("broadcaster", "b", PulseType.LOW),
        Pulse("broadcaster", "c", PulseType.LOW),
        Pulse("a", "b", PulseType.HIGH),
        Pulse("b", "c", PulseType.HIGH),
        Pulse("c", "inv", PulseType.HIGH),
        Pulse("inv", "a", PulseType.LOW),
        Pulse("a", "b", PulseType.LOW),
        Pulse("b", "c", PulseType.LOW),
        Pulse("c", "inv", PulseType.LOW),
        Pulse("inv", "a", PulseType.HIGH),
    ]


def test_module_network_has_its_state_changed_after_propagation():
    network = _example_network_2()
    monitor = PulseHistory()
    initial_pulse = Pulse("button", "broadcaster", PulseType.LOW)
    network.propagate(initial_pulse, monitor)
    network.propagate(initial_pulse, monitor)
    pulses = list(monitor.history())
    assert pulses == [
        # 1st button press
        Pulse("button", "broadcaster", PulseType.LOW),
        Pulse("broadcaster", "a", PulseType.LOW),
        Pulse("a", "inv", PulseType.HIGH),
        Pulse("a", "con", PulseType.HIGH),
        Pulse("inv", "b", PulseType.LOW),
        Pulse("con", "output", PulseType.HIGH),
        Pulse("b", "con", PulseType.HIGH),
        Pulse("con", "output", PulseType.LOW),
        # 2nd button press
        Pulse("button", "broadcaster", PulseType.LOW),
        Pulse("broadcaster", "a", PulseType.LOW),
        Pulse("a", "inv", PulseType.LOW),
        Pulse("a", "con", PulseType.LOW),
        Pulse("inv", "b", PulseType.HIGH),
        Pulse("con", "output", PulseType.HIGH),
    ]
