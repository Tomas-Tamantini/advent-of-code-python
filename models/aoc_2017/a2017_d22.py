from models.vectors import Vector2D, CardinalDirection
from models.cellular_automata import LangtonsAnt, AntState


class GridCluster:
    def __init__(
        self,
        carrier_position: Vector2D,
        carrier_direction: CardinalDirection,
        currently_infected: set[Vector2D],
    ) -> None:
        self._carrier_position = carrier_position
        self._carrier_direction = carrier_direction
        self._currently_infected = currently_infected

    @property
    def _langtons_ant(self) -> LangtonsAnt:
        return LangtonsAnt(
            ant_state=AntState(
                position=self._carrier_position,
                direction=self._carrier_direction,
            ),
            initial_on_squares={p for p in self._currently_infected},
        )

    def total_number_of_infections_caused(self, number_of_steps: int) -> int:
        total = 0
        ant = self._langtons_ant
        for _ in range(number_of_steps):
            if ant.position not in ant.on_squares:
                total += 1
            ant.walk()
        return total
