import pytest
from ..bridge_builder import MagneticBridge, BridgeComponent, BridgeBuilder


def test_bridge_starts_with_zero_strength():
    assert MagneticBridge().strength == 0


def test_cannot_connect_non_zero_pins_component_to_empty_bridge():
    component = BridgeComponent(1, 2)
    with pytest.raises(ValueError):
        MagneticBridge().connect(component)


def test_can_connect_zero_pin_component_to_empty_bridge():
    component = BridgeComponent(0, 2)
    bridge = MagneticBridge().connect(component)
    assert bridge.strength == 2


def test_strongest_build_with_no_available_components_has_strength_zero():
    components = []
    builder = BridgeBuilder(components)
    builder.build()
    assert builder.max_strength == 0


def test_strongest_bridge_with_no_zero_pin_components_has_strength_zero():
    components = [BridgeComponent(1, 2)]
    builder = BridgeBuilder(components)
    builder.build()
    assert builder.max_strength == 0


def test_strongest_bridge_is_returned():
    components = [
        BridgeComponent(0, 10),
        BridgeComponent(0, 9),
        BridgeComponent(9, 1),
        BridgeComponent(9, 2),
    ]
    builder = BridgeBuilder(components)
    builder.build()
    assert builder.max_strength == 20


def test_max_strength_of_longest_bridge_is_returned():
    components = [
        BridgeComponent(0, 2),
        BridgeComponent(2, 2),
        BridgeComponent(2, 3),
        BridgeComponent(3, 4),
        BridgeComponent(3, 5),
        BridgeComponent(0, 1),
        BridgeComponent(10, 1),
        BridgeComponent(9, 10),
    ]
    builder = BridgeBuilder(components)
    builder.build()
    assert builder.max_strength == 31
    assert builder.max_strength_of_longest_bridge == 19
