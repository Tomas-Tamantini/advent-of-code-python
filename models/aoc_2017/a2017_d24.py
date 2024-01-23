from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class BridgeComponent:
    num_pins_port_a: int
    num_pins_port_b: int

    @property
    def strength(self) -> int:
        return self.num_pins_port_a + self.num_pins_port_b


class MagneticBridge:
    def __init__(self, num_pins_last_port: int = 0, strength: int = 0) -> None:
        self._num_pins_last_port = num_pins_last_port
        self._strength = strength

    @property
    def strength(self) -> int:
        return self._strength

    def connect(self, component: BridgeComponent) -> "MagneticBridge":
        if component.num_pins_port_a == self._num_pins_last_port:
            return MagneticBridge(
                num_pins_last_port=component.num_pins_port_b,
                strength=self._strength + component.strength,
            )
        elif component.num_pins_port_b == self._num_pins_last_port:
            return MagneticBridge(
                num_pins_last_port=component.num_pins_port_a,
                strength=self._strength + component.strength,
            )
        else:
            raise ValueError("Cannot connect component ")


def _bridge_strength_recursive(
    bridge: MagneticBridge, components: list[BridgeComponent]
) -> Iterator[int]:
    yield bridge.strength
    for component in components:
        try:
            yield from _bridge_strength_recursive(
                bridge.connect(component), [c for c in components if c != component]
            )
        except ValueError:
            pass


def max_bridge_strength(components: list[BridgeComponent]) -> int:
    current_bridge = MagneticBridge()
    return max(_bridge_strength_recursive(current_bridge, components))
