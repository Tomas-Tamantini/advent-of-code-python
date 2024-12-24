import pytest

from ..logic import AndGate, OrGate, XorGate, swapped_pair_of_wires_for_full_adder


@pytest.mark.skip("Not implemented")
def test_swapped_pair_of_wires_for_half_adder_are_detected():
    add_gate = XorGate("x00", "y00", "z00")
    carry_gate = AndGate("x00", "y00", "c00")
    gates = [add_gate, carry_gate]
    pairs = list(swapped_pair_of_wires_for_full_adder(gates))
    assert pairs == [{"c00", "z00"}]


@pytest.mark.skip("Not implemented")
def test_proper_full_adder_has_no_swapped_wires():
    # Half adder
    add_0 = XorGate("x00", "y00", "z00")
    carry_0 = AndGate("x00", "y00", "c00")

    # Full adder
    add_1a = XorGate("x01", "y01", "a01")
    carry_1b = AndGate("x01", "y01", "b01")

    carry_1d = AndGate("a01", "c00", "d01")
    add_1z = XorGate("a01", "c00", "z01")

    carry_1c = OrGate("b01", "d01", "c01")

    gates = [add_0, carry_0, add_1a, add_1z, carry_1b, carry_1d, carry_1c]
    pairs = list(swapped_pair_of_wires_for_full_adder(gates))
    assert pairs == []


@pytest.mark.skip("Not implemented")
def test_swapped_pair_of_wires_for_full_adder_are_detected():
    # Half adder
    add_0 = XorGate("x00", "y00", "z02")
    carry_0 = AndGate("x00", "y00", "c00")

    # Full adders
    add_1a = XorGate("x01", "y01", "b01")
    carry_1b = AndGate("x01", "y01", "a01")
    carry_1d = AndGate("a01", "c00", "z01")
    carry_1c = OrGate("b01", "d01", "c01")
    add_1z = XorGate("a01", "c00", "d01")

    add_2a = XorGate("x02", "y02", "a02")
    carry_2b = AndGate("x02", "y02", "b02")
    carry_2d = AndGate("a02", "c01", "d02")
    carry_2c = OrGate("b02", "d02", "c02")
    add_2z = XorGate("a02", "c01", "z00")

    gates = [
        add_0,
        carry_0,
        add_1a,
        add_1z,
        carry_1b,
        carry_1d,
        carry_1c,
        add_2a,
        add_2z,
        carry_2b,
        carry_2d,
        carry_2c,
    ]
    pairs = list(swapped_pair_of_wires_for_full_adder(gates))
    assert pairs == [{"a01", "b01"}, {"z01", "d01"}, {"z02", "z00"}]
