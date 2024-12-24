from ..logic import AndGate, Circuit, OrGate, Pulse, PulseType, XorGate

"""
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""


def test_circuit_propagates_input_pulses():
    circuit = Circuit(
        gates=[
            AndGate("x00", "y00", "z00"),
            XorGate("x01", "y01", "z01"),
            OrGate("x02", "y02", "z02"),
        ]
    )
    input_pulses = [
        Pulse("x00", PulseType.HIGH),
        Pulse("x01", PulseType.HIGH),
        Pulse("x02", PulseType.HIGH),
        Pulse("y00", PulseType.LOW),
        Pulse("y01", PulseType.HIGH),
        Pulse("y02", PulseType.LOW),
    ]
    output_pulses = set(circuit.propagate(input_pulses))
    assert output_pulses == {
        Pulse("z00", PulseType.LOW),
        Pulse("z01", PulseType.LOW),
        Pulse("z02", PulseType.HIGH),
    } | set(input_pulses)
