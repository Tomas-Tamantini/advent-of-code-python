from dataclasses import dataclass
from typing import Iterator, Optional

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

    def is_complete(self) -> bool:
        return (
            self._pointers.contiguous_group_pointer >= self._row.num_groups
            and self._pointers.cell_pointer >= self._row.num_cells
        )

    def _there_are_remaining_groups(self) -> bool:
        return self._row.num_groups - self._pointers.contiguous_group_pointer > 0

    def _current_cell(self) -> Optional[chr]:
        return (
            self._row.cells[self._pointers.cell_pointer]
            if self._pointers.cell_pointer < self._row.num_cells
            else None
        )

    def _current_group_size(self) -> int:
        return self._row.contiguous_groups_sizes[
            self._pointers.contiguous_group_pointer
        ]

    def _skip_current_cell(self) -> _NonogramSolvePointers:
        return _NonogramSolvePointers(
            cell_pointer=self._pointers.cell_pointer + 1,
            contiguous_group_pointer=self._pointers.contiguous_group_pointer,
        )

    def _fill_in_current_cell(self) -> _NonogramSolvePointers:
        return _NonogramSolvePointers(
            self._pointers.cell_pointer + self._current_group_size() + 1,
            self._pointers.contiguous_group_pointer + 1,
        )

    def _can_skip_current_cell(self) -> bool:
        return self._current_cell() in (_EMPTY, _UNKNOWN)

    def _can_fill_in_current_cell(self) -> bool:
        if not self._there_are_remaining_groups() or self._current_cell() not in (
            _FILLED_IN,
            _UNKNOWN,
        ):
            return False
        current_group_size = self._current_group_size()
        if self._pointers.cell_pointer + current_group_size > self._row.num_cells:
            return False

        substring = self._row.cells[
            self._pointers.cell_pointer : self._pointers.cell_pointer
            + current_group_size
        ]
        if _EMPTY in substring:
            return False

        next_index = self._pointers.cell_pointer + current_group_size

        if (next_index < self._row.num_cells) and self._row.cells[
            next_index
        ] == _FILLED_IN:
            return False

        return True

    def _next_pointers(self) -> Iterator[_NonogramSolvePointers]:
        if self._can_skip_current_cell():
            yield self._skip_current_cell()
        if self._can_fill_in_current_cell():
            yield self._fill_in_current_cell()

    def next_states(self) -> Iterator["_NonogramSolveState"]:
        for next_pointers in self._next_pointers():
            yield _NonogramSolveState(self._row, next_pointers)


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
    if state.is_complete():
        num_arrangements = 1
    else:
        num_arrangements = sum(
            _num_arrangements_recursive(next_state, memoized_results)
            for next_state in state.next_states()
        )

    memoized_results[state.pointers] = num_arrangements
    return num_arrangements
