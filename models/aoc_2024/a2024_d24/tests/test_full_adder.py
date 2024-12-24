from ..logic import (
    AndGate,
    Circuit,
    OrGate,
    XorGate,
    swapped_pair_of_wires_for_full_adder,
)


def test_proper_full_adder_has_no_swapped_wires():
    circuit = Circuit(
        [
            # Half adder
            XorGate("x00", "y00", "z00"),
            AndGate("x00", "y00", "c00"),
            # Full adder
            XorGate("x01", "y01", "a01"),
            AndGate("x01", "y01", "b01"),
            AndGate("a01", "c00", "d01"),
            XorGate("a01", "c00", "z01"),
            OrGate("b01", "d01", "c01"),
        ]
    )
    pairs = list(swapped_pair_of_wires_for_full_adder(circuit))
    assert pairs == []


def test_swapped_pair_of_wires_for_full_adder_are_detected():
    # Half adder
    circuit = Circuit(
        [
            # Half adder
            XorGate("x00", "y00", "z00"),
            AndGate("x00", "y00", "c00"),
            # First full adder
            XorGate("x01", "y01", "b01"),
            AndGate("x01", "y01", "a01"),
            XorGate("a01", "c00", "z01"),
            AndGate("a01", "c00", "d01"),
            OrGate("b01", "d01", "c01"),
            # Second full adder
            XorGate("x02", "y02", "a02"),
            AndGate("x02", "y02", "b02"),
            XorGate("a02", "c01", "d02"),
            AndGate("a02", "c01", "z02"),
            OrGate("b02", "d02", "c02"),
        ]
    )
    pairs = list(swapped_pair_of_wires_for_full_adder(circuit))
    assert pairs == [{"a01", "b01"}, {"z02", "d02"}]
