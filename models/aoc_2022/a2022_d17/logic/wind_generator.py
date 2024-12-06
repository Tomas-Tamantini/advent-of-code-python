from dataclasses import dataclass

from models.common.vectors import CardinalDirection


@dataclass(frozen=True)
class WindGenerator:
    directions: tuple[CardinalDirection]
    current_index: int = 0

    def _incremented_index(self, index_offset: int) -> int:
        return (self.current_index + index_offset) % len(self.directions)

    def wind_direction(self, index_offset: int = 0) -> CardinalDirection:
        return self.directions[self._incremented_index(index_offset)]

    def increment(self, index_offset: int = 1) -> "WindGenerator":
        return WindGenerator(
            directions=self.directions,
            current_index=self._incremented_index(index_offset),
        )
