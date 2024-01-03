import pytest
from models.aoc_2015 import (
    LogicGatesCircuit,
    DoNothingGate,
    AndGate,
    OrGate,
    LeftShiftGate,
    RightShiftGate,
    NotGate,
)


def test_do_nothing_gate_just_passes_signal_along():
    gate = DoNothingGate()
    gate.add_input_signal(123)
    assert gate.evaluate() == 123


def test_and_gate_does_bitwise_and():
    gate = AndGate()
    gate.add_input_signal(123)
    gate.add_input_wire("x")
    assert gate.evaluate({"x": 456}) == 72


def test_or_gate_does_bitwise_or():
    gate = OrGate()
    gate.add_input_wire("x")
    gate.add_input_wire("y")
    assert gate.evaluate({"x": 156, "y": 52}) == 188


def test_left_shift_gate_shifts_n_bits():
    gate = LeftShiftGate(shift=3, num_bits=16)
    gate.add_input_wire("x")
    assert gate.evaluate({"x": 39}) == 312


def test_left_shift_does_not_exceed_number_of_bits():
    gate = LeftShiftGate(shift=1, num_bits=2)
    gate.add_input_signal(3)
    assert gate.evaluate() == 2


def test_right_shift_gate_shifts_n_bits():
    gate = RightShiftGate(shift=2, num_bits=16)
    gate.add_input_wire("x")
    assert gate.evaluate({"x": 157}) == 39


def test_right_shift_ignores_extra_bits_in_input():
    gate = RightShiftGate(shift=1, num_bits=2)
    gate.add_input_signal(4)
    assert gate.evaluate() == 0


def test_not_gate_does_bitwise_not():
    gate = NotGate(num_bits=16)
    gate.add_input_wire("x")
    assert gate.evaluate({"x": 123}) == 65412


def test_same_wire_cannot_be_output_of_two_gates():
    circuit = LogicGatesCircuit()
    circuit.add_gate(gate=DoNothingGate(), output_wire="x")
    with pytest.raises(ValueError):
        circuit.add_gate(DoNothingGate(), output_wire="x")


def test_circuit_computes_signals_in_order():
    circuit = LogicGatesCircuit()

    assign_x_gate = DoNothingGate()
    assign_x_gate.add_input_signal(123)
    circuit.add_gate(assign_x_gate, "x")

    assign_y_gate = DoNothingGate()
    assign_y_gate.add_input_signal(456)
    circuit.add_gate(assign_y_gate, "y")

    and_gate = AndGate()
    and_gate.add_input_wire("x")
    and_gate.add_input_wire("y")
    circuit.add_gate(and_gate, "d")

    or_gate = OrGate()
    or_gate.add_input_wire("x")
    or_gate.add_input_wire("y")
    circuit.add_gate(or_gate, "e")

    left_shift_gate = LeftShiftGate(shift=2, num_bits=16)
    left_shift_gate.add_input_wire("x")
    circuit.add_gate(left_shift_gate, "f")

    right_shift_gate = RightShiftGate(shift=2, num_bits=16)
    right_shift_gate.add_input_wire("y")
    circuit.add_gate(right_shift_gate, "g")

    not_x_gate = NotGate(num_bits=16)
    not_x_gate.add_input_wire("x")
    circuit.add_gate(not_x_gate, "h")

    not_y_gate = NotGate(num_bits=16)
    not_y_gate.add_input_wire("y")
    circuit.add_gate(not_y_gate, "i")

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


def test_can_override_value_in_circuit():
    circuit = LogicGatesCircuit()

    assign_x_gate = DoNothingGate()
    assign_x_gate.add_input_signal(1)
    circuit.add_gate(assign_x_gate, "x")

    not_x_gate = NotGate(num_bits=3)
    not_x_gate.add_input_wire("x")
    circuit.add_gate(not_x_gate, "y")

    assert circuit.get_value("y", override_values={"x": 3}) == 4
