from dataclasses import dataclass


@dataclass(frozen=True)
class TeleportNanobot:
    radius: int
    position: tuple[int, int, int]

    def is_in_range(self, position: tuple[int, int, int]) -> bool:
        dist = [abs(a - b) for a, b in zip(self.position, position)]
        return sum(dist) <= self.radius
