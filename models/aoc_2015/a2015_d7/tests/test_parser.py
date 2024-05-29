from models.common.io import InputFromString
from ..parser import parse_logic_gates_circuit


def test_parse_logic_gates_circuit():
    input_reader = InputFromString(
        """123 -> x
           456 -> y
           x AND y -> d
           x OR y -> e
           x LSHIFT 2 -> f
           y RSHIFT 2 -> g
           NOT x -> h
           NOT y -> i"""
    )
    circuit = parse_logic_gates_circuit(input_reader)
    expected_values = {
        "x": 123,
        "y": 456,
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
    }
    for wire, value in expected_values.items():
        assert circuit.get_value(wire) == value
