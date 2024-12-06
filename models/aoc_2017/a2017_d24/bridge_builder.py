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
    def __init__(
        self, num_pins_last_port: int = 0, strength: int = 0, length: int = 0
    ) -> None:
        self._num_pins_last_port = num_pins_last_port
        self._strength = strength
        self._length = length

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def length(self) -> int:
        return self._length

    def connect(self, component: BridgeComponent) -> "MagneticBridge":
        if component.num_pins_port_a == self._num_pins_last_port:
            return MagneticBridge(
                num_pins_last_port=component.num_pins_port_b,
                strength=self._strength + component.strength,
                length=self._length + 1,
            )
        elif component.num_pins_port_b == self._num_pins_last_port:
            return MagneticBridge(
                num_pins_last_port=component.num_pins_port_a,
                strength=self._strength + component.strength,
                length=self._length + 1,
            )
        else:
            raise ValueError("Cannot connect component ")


class BridgeBuilder:
    def __init__(self, components: list[BridgeComponent]) -> None:
        self._components = components
        self._max_strength = 0
        self._max_length = (0, 0)

    @property
    def max_strength(self) -> int:
        return self._max_strength

    @property
    def max_strength_of_longest_bridge(self) -> int:
        return self._max_length[1]

    @staticmethod
    def _build_recursive(
        bridge: MagneticBridge, components: list[BridgeComponent]
    ) -> Iterator[MagneticBridge]:
        could_connect_some = False
        for component in components:
            try:
                yield from BridgeBuilder._build_recursive(
                    bridge.connect(component), [c for c in components if c != component]
                )
                could_connect_some = True
            except ValueError:
                pass
        if not could_connect_some:
            yield bridge

    def build(self) -> None:
        # TODO: Optimize (maybe with memoization?)
        current_bridge = MagneticBridge()
        for bridge in self._build_recursive(current_bridge, self._components):
            self._max_strength = max(bridge.strength, self._max_strength)
            self._max_length = max((bridge.length, bridge.strength), self._max_length)
