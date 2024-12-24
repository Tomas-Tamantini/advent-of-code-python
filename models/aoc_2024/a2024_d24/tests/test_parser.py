from models.common.io import InputFromString

from ..logic import AndGate, OrGate, Pulse, PulseType, XorGate
from ..parser import parse_input_pulses, parse_logic_gates

_FILE_CONTENT = """
                x00: 1
                x01: 1
                x02: 1
                y00: 0
                y01: 1
                y02: 0

                x00 AND y00 -> z00
                x01 XOR y01 -> z01
                x02 OR y02 -> z02
                """


def test_parse_logic_gates():
    input_reader = InputFromString(_FILE_CONTENT)
    gates = list(parse_logic_gates(input_reader))
    assert gates == [
        AndGate(wire_input_a="x00", wire_input_b="y00", wire_output="z00"),
        XorGate(wire_input_a="x01", wire_input_b="y01", wire_output="z01"),
        OrGate(wire_input_a="x02", wire_input_b="y02", wire_output="z02"),
    ]


def test_parse_input_pulses():
    input_reader = InputFromString(_FILE_CONTENT)
    pulses = list(parse_input_pulses(input_reader))
    assert pulses == [
        Pulse(wire="x00", pulse_type=PulseType.HIGH),
        Pulse(wire="x01", pulse_type=PulseType.HIGH),
        Pulse(wire="x02", pulse_type=PulseType.HIGH),
        Pulse(wire="y00", pulse_type=PulseType.LOW),
        Pulse(wire="y01", pulse_type=PulseType.HIGH),
        Pulse(wire="y02", pulse_type=PulseType.LOW),
    ]
