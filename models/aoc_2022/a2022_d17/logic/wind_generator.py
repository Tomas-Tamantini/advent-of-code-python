from itertools import cycle
from models.common.vectors import CardinalDirection


class WindGenerator:
    def __init__(self, directions: list[CardinalDirection]) -> None:
        self.directions = cycle(directions)

    def next_wind_direction(self) -> CardinalDirection:
        return next(self.directions)
