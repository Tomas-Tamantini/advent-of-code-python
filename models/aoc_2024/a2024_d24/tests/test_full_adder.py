from ..logic import AndGate, OrGate, XorGate, swapped_pair_of_wires_for_full_adder


def test_swapped_pair_of_wires_for_half_adder_are_detected():
    add_gate = XorGate("x00", "y00", "z00")
    carry_gate = AndGate("x00", "y00", "c00")
    gates = [add_gate, carry_gate]
    pairs = list(swapped_pair_of_wires_for_full_adder(gates))
    assert pairs == [{"c00", "z00"}]


def test_swapped_pair_of_wires_for_full_adder_are_detected():
    # Half adder
    add_0 = XorGate("x00", "y00", "z00")
    carry_0 = AndGate("x00", "y00", "c00")

    # Full adder with 2 output swaps
    add_1a = XorGate("x01", "y01", "b01")
    carry_1b = AndGate("x01", "y01", "a01")
    carry_1d = AndGate("a01", "c00", "z01")
    carry_1c = OrGate("b01", "d01", "c01")
    add_1z = XorGate("a01", "c00", "d01")

    gates = [add_0, carry_0, add_1a, add_1z, carry_1b, carry_1d, carry_1c]
    pairs = list(swapped_pair_of_wires_for_full_adder(gates))
    assert pairs == [{"a01", "b01"}, {"z01", "d01"}]
