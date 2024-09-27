from models.common.vectors import CardinalDirection


class PipeSegment:
    def __init__(self, direction_a: CardinalDirection, direction_b: CardinalDirection):
        self._directions = {direction_a, direction_b}

    def can_enter_from(self, direction: CardinalDirection) -> bool:
        return direction in self._directions

    def exit_direction(self, enter_direction: CardinalDirection) -> CardinalDirection:
        return next(iter(self._directions - {enter_direction.reverse()}))
