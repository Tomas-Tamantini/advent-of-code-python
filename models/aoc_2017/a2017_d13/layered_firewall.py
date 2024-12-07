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
        t %= 2 * self._scanning_range - 2
        return self._scanning_range - 1 - abs(t - self._scanning_range + 1)


class LayeredFirewall:
    def __init__(self, layers: dict[int, FirewallLayer]) -> None:
        self._layers = layers

    def packet_collisions(self) -> Iterator[tuple[int, FirewallLayer]]:
        for layer_depth, layer in self._layers.items():
            if layer.scanner_position_at_time(layer_depth) == 0:
                yield layer_depth, layer

    def minimum_delay_to_avoid_collisions(self) -> int:
        candidates = [True for _ in range(5_000_000)]
        already_calculated = set()
        for layer_depth, layer in self._layers.items():
            first_term = (-layer_depth) % (2 * layer.scanning_range - 2)
            if (first_term, layer.scanning_range) in already_calculated:
                continue
            already_calculated.add((first_term, layer.scanning_range))
            for t in range(first_term, len(candidates), 2 * layer.scanning_range - 2):
                candidates[t] = False
        try:
            return candidates.index(True)
        except ValueError:
            raise ValueError("No delay found")
