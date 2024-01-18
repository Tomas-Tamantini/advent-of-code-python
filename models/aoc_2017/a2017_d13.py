from typing import Iterator


class FirewallLayer:
    def __init__(self, scanning_range: int = 0) -> None:
        self._scanning_range = scanning_range

    @property
    def scanning_range(self) -> int:
        return self._scanning_range

    def scanner_position_at_time(self, t: int) -> int:
        if not self._scanning_range:
            return -1
        if self._scanning_range == 1:
            return 0
        t = t % (2 * self._scanning_range - 2)
        return self._scanning_range - 1 - abs(t - self._scanning_range + 1)


class LayeredFirewall:
    def __init__(self, layers: dict[int, FirewallLayer]) -> None:
        self._layers = layers

    def packet_collisions(self) -> Iterator[tuple[int, FirewallLayer]]:
        for layer_depth, layer in self._layers.items():
            if layer.scanner_position_at_time(layer_depth) == 0:
                yield layer_depth, layer
