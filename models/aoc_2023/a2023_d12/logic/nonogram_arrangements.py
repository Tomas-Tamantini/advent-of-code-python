from typing import Optional
from dataclasses import dataclass
from .nonogram_row import NonogramRow


_FILLED_IN = "#"
_EMPTY = "."
_UNKNOWN = "?"


@dataclass(frozen=True)
class _NonogramSolvePointers:
    cell_pointer: int
    contiguous_group_pointer: int


class _NonogramSolveState:
    def __init__(self, row: NonogramRow, pointers: _NonogramSolvePointers) -> None:
        self._row = row
        self._pointers = pointers

    @property
    def pointers(self) -> _NonogramSolvePointers:
        return self._pointers

    def filled_in_all_groups(self) -> bool:
        return self._pointers.contiguous_group_pointer >= self._row.num_groups

    def some_filled_in_cell_ahead(self) -> bool:
        substring_ahead = self._row.cells[self._pointers.cell_pointer :]
        return _FILLED_IN in substring_ahead

    def current_cell(self) -> Optional[chr]:
        return (
            self._row.cells[self._pointers.cell_pointer]
            if self._pointers.cell_pointer < self._row.num_cells
            else None
        )

    def state_after_filling_in_current_group(
        self,
    ) -> Optional["_NonogramSolveState"]:
        current_group_size = self._row.contiguous_groups_sizes[
            self._pointers.contiguous_group_pointer
        ]
        if self._pointers.cell_pointer + current_group_size > self._row.num_cells:
            return None

        substring = self._row.cells[
            self._pointers.cell_pointer : self._pointers.cell_pointer
            + current_group_size
        ]
        if _EMPTY in substring:
            return None

        next_index = self._pointers.cell_pointer + current_group_size

        if (next_index < self._row.num_cells) and self._row.cells[
            next_index
        ] == _FILLED_IN:
            return None

        pointers = _NonogramSolvePointers(
            self._pointers.cell_pointer + current_group_size + 1,
            self._pointers.contiguous_group_pointer + 1,
        )
        return _NonogramSolveState(self._row, pointers)

    def increment_cell_pointer(self) -> "_NonogramSolveState":
        pointers = _NonogramSolvePointers(
            self._pointers.cell_pointer + 1, self._pointers.contiguous_group_pointer
        )
        return _NonogramSolveState(self._row, pointers)


def num_arrangements_nonogram_row(row: NonogramRow) -> int:
    memoized_results = dict()
    initial_pointers = _NonogramSolvePointers(
        cell_pointer=0, contiguous_group_pointer=0
    )
    initial_state = _NonogramSolveState(row, initial_pointers)
    return _num_arrangements_recursive(initial_state, memoized_results)


def _num_arrangements_recursive(
    state: _NonogramSolveState, memoized_results: dict[_NonogramSolvePointers, int]
) -> int:
    if state.pointers in memoized_results:
        return memoized_results[state.pointers]
    num_arrangements = 0
    if state.filled_in_all_groups():
        num_arrangements = 0 if state.some_filled_in_cell_ahead() else 1
    else:
        num_arrangements = _num_arrangements_with_remaining_groups(
            state, memoized_results
        )

    memoized_results[state.pointers] = num_arrangements
    return num_arrangements


def _num_arrangements_with_remaining_groups(
    state: _NonogramSolveState, memoized_results: dict[_NonogramSolvePointers, int]
) -> int:
    current_cell = state.current_cell()
    if current_cell == _EMPTY:
        new_state = state.increment_cell_pointer()
        return _num_arrangements_recursive(new_state, memoized_results)
    elif current_cell == _FILLED_IN:
        new_state = state.state_after_filling_in_current_group()
        return (
            0
            if new_state is None
            else _num_arrangements_recursive(new_state, memoized_results)
        )
    elif current_cell == _UNKNOWN:
        state_without_filling_in = state.increment_cell_pointer()
        num_without_filling_in = _num_arrangements_recursive(
            state_without_filling_in, memoized_results
        )
        state_filling_in = state.state_after_filling_in_current_group()
        num_filling_in = (
            0
            if state_filling_in is None
            else _num_arrangements_recursive(state_filling_in, memoized_results)
        )
        return num_without_filling_in + num_filling_in
    else:
        return 0
