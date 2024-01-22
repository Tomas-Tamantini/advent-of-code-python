from dataclasses import dataclass
from typing import Hashable
from enum import Enum
from models.vectors import Vector2D, CardinalDirection

CellState = Hashable


class AntTurnDirection(Enum):  # TODO: Extract to models/vectors.py
    LEFT = "L"
    RIGHT = "R"
    NO_TURN = "N"
    U_TURN = "U"

    def transform_direction(self, direction: CardinalDirection) -> CardinalDirection:
        if self == AntTurnDirection.LEFT:
            return direction.turn_left()
        elif self == AntTurnDirection.RIGHT:
            return direction.turn_right()
        elif self == AntTurnDirection.NO_TURN:
            return direction
        else:
            return direction.reverse()


@dataclass(frozen=True)
class AntState:
    position: Vector2D
    direction: CardinalDirection


class MultiCellStateLangtonsAnt:
    def __init__(
        self,
        ant_state: AntState,
        cells: dict[Vector2D, CellState],
        default_state: CellState,
        rule: dict[CellState, tuple[CellState, AntTurnDirection]],
    ) -> None:
        self._ant_state = ant_state
        self._default_state = default_state
        self._cells = cells
        self._rule = rule

    @property
    def current_cell(self) -> CellState:
        return self._cells.get(self.position, self._default_state)

    @property
    def position(self) -> Vector2D:
        return self._ant_state.position

    @property
    def direction(self) -> CardinalDirection:
        return self._ant_state.direction

    def walk(self) -> None:
        new_state, turn_direction = self._rule[self.current_cell]
        if new_state == self._default_state:
            self._cells.pop(self.position)
        else:
            self._cells[self.position] = new_state
        new_direction = turn_direction.transform_direction(self._ant_state.direction)
        self._ant_state = AntState(self.position.move(new_direction), new_direction)


class LangtonsAnt(MultiCellStateLangtonsAnt):
    def __init__(
        self,
        ant_state: AntState,
        initial_on_cells: set[Vector2D],
    ) -> None:
        default_state = 0
        cells = {square: 1 for square in initial_on_cells}
        rule = {
            0: (1, AntTurnDirection.RIGHT),
            1: (0, AntTurnDirection.LEFT),
        }
        super().__init__(ant_state, cells, default_state, rule)

    @property
    def on_cells(self) -> set[Vector2D]:
        return set(self._cells.keys())
