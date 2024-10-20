from models.common.io import InputFromString
from ..parser import parse_module_network
from ..logic import Pulse, PulseType, PulseHistory


def test_parse_module_network():
    file_content = """broadcaster -> a
                      %a -> inv, con
                      &inv -> b
                      %b -> con
                      &con -> output"""
    input_reader = InputFromString(file_content)
    network = parse_module_network(input_reader)
    monitor = PulseHistory()
    initial_pulse = Pulse("button", "broadcaster", PulseType.LOW)
    network.propagate(initial_pulse, monitor)
    pulses = list(monitor.history())
    assert pulses == [
        Pulse("button", "broadcaster", PulseType.LOW),
        Pulse("broadcaster", "a", PulseType.LOW),
        Pulse("a", "inv", PulseType.HIGH),
        Pulse("a", "con", PulseType.HIGH),
        Pulse("inv", "b", PulseType.LOW),
        Pulse("con", "output", PulseType.HIGH),
        Pulse("b", "con", PulseType.HIGH),
        Pulse("con", "output", PulseType.LOW),
    ]
