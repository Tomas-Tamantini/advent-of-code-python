from enum import Enum
from typing import Optional

from models.common.cellular_automata import AntState, LangtonsAnt, MultiStateLangtonsAnt
from models.common.io import ProgressBar
from models.common.vectors import CardinalDirection, TurnDirection, Vector2D


class CellState(int, Enum):
    CLEAN = 0
    INFECTED = 1
    WEAKENED = 2
    FLAGGED = 3


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

    def _langtons_ant(self, use_four_states: bool) -> MultiStateLangtonsAnt:
        ant_state = AntState(
            position=self._carrier_position,
            direction=self._carrier_direction,
        )
        if not use_four_states:
            return LangtonsAnt(
                ant_state=ant_state,
                initial_on_cells={p for p in self._currently_infected},
            )
        else:
            default_state = CellState.CLEAN
            cells = {pos: CellState.INFECTED for pos in self._currently_infected}
            rule = {
                CellState.CLEAN: (CellState.WEAKENED, TurnDirection.RIGHT),
                CellState.WEAKENED: (CellState.INFECTED, TurnDirection.NO_TURN),
                CellState.INFECTED: (CellState.FLAGGED, TurnDirection.LEFT),
                CellState.FLAGGED: (CellState.CLEAN, TurnDirection.U_TURN),
            }
            return MultiStateLangtonsAnt(
                ant_state=ant_state,
                cells=cells,
                default_state=default_state,
                rule=rule,
            )

    def total_number_of_infections_caused(
        self,
        number_of_steps: int,
        use_four_states: bool = False,
        progress_bar: Optional[ProgressBar] = None,
    ) -> int:
        total = 0
        ant = self._langtons_ant(use_four_states)
        for step in range(number_of_steps):
            if progress_bar is not None:
                progress_bar.update(step, number_of_steps)
            old_position = ant.position
            ant.walk()
            if ant.cell_state(old_position) == CellState.INFECTED:
                total += 1
        return total
