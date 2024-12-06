from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional

from models.common.number_theory import Interval


@dataclass(frozen=True)
class TicketFieldValidator:
    field_name: str
    intervals: tuple[Interval, ...]

    def is_valid(self, value: int) -> bool:
        return any(interval.contains(value) for interval in self.intervals)


class _CorrespondenceStatus(int, Enum):
    UNKNOWN = 0
    CORRESPONDS = 1
    DOES_NOT_CORRESPOND = 2


class _CorrespondenceMatrix:
    def __init__(self, size: int) -> None:
        self._values = [
            [_CorrespondenceStatus.UNKNOWN for _ in range(size)] for _ in range(size)
        ]
        self._reduction_stack = []

    def cells_which_correspond(self) -> Iterator[tuple[int, int]]:
        for row_idx, row in enumerate(self._values):
            for col_idx, status in enumerate(row):
                if status == _CorrespondenceStatus.CORRESPONDS:
                    yield row_idx, col_idx

    def _status_count_in_row(self, row_idx: int, status: _CorrespondenceStatus) -> int:
        return self._values[row_idx].count(status)

    def _status_count_in_column(
        self, col_idx: int, status: _CorrespondenceStatus
    ) -> int:
        return [row[col_idx] for row in self._values].count(status)

    def _deduce_match_in_row(self, row_idx: int) -> Optional[int]:
        if (
            self._status_count_in_row(row_idx, _CorrespondenceStatus.UNKNOWN) == 1
            and self._status_count_in_row(row_idx, _CorrespondenceStatus.CORRESPONDS)
            == 0
        ):
            return self._values[row_idx].index(_CorrespondenceStatus.UNKNOWN)

    def _deduce_match_in_column(self, col_idx: int) -> Optional[int]:
        if (
            self._status_count_in_column(col_idx, _CorrespondenceStatus.UNKNOWN) == 1
            and self._status_count_in_column(col_idx, _CorrespondenceStatus.CORRESPONDS)
            == 0
        ):
            return [row[col_idx] for row in self._values].index(
                _CorrespondenceStatus.UNKNOWN
            )

    def _try_deduce_match(self, row_idx, col_idx):
        if (match_col_idx := self._deduce_match_in_row(row_idx)) is not None:
            self.set_correspondence(
                row_idx, match_col_idx, _CorrespondenceStatus.CORRESPONDS
            )
        elif (match_row_idx := self._deduce_match_in_column(col_idx)) is not None:
            self.set_correspondence(
                match_row_idx, col_idx, _CorrespondenceStatus.CORRESPONDS
            )

    def _eliminate_others_in_row_and_col(self, row_idx, col_idx):
        for i in range(len(self._values)):
            if i != row_idx:
                self.set_correspondence(
                    i, col_idx, _CorrespondenceStatus.DOES_NOT_CORRESPOND
                )
        for i in range(len(self._values[row_idx])):
            if i != col_idx:
                self.set_correspondence(
                    row_idx, i, _CorrespondenceStatus.DOES_NOT_CORRESPOND
                )

    def _reduce(self) -> None:
        while self._reduction_stack:
            row_idx, col_idx = self._reduction_stack.pop()
            status = self._values[row_idx][col_idx]
            if status == _CorrespondenceStatus.CORRESPONDS:
                self._eliminate_others_in_row_and_col(row_idx, col_idx)
            elif status == _CorrespondenceStatus.DOES_NOT_CORRESPOND:
                self._try_deduce_match(row_idx, col_idx)

    def set_correspondence(
        self, row: int, col: int, status: _CorrespondenceStatus
    ) -> None:
        if self._values[row][col] != status:
            self._values[row][col] = status
            self._reduction_stack.append((row, col))
            self._reduce()


@dataclass(frozen=True)
class TicketValidator:
    field_validators: tuple[TicketFieldValidator, ...]

    def is_valid_field(self, value: int) -> bool:
        return any(
            field_validator.is_valid(value) for field_validator in self.field_validators
        )

    def is_valid_ticket(self, ticket: tuple[int]) -> bool:
        return all(self.is_valid_field(value) for value in ticket)

    def _valid_tickets(self, tickets: list[tuple[int]]) -> Iterator[tuple[int]]:
        for ticket in tickets:
            if self.is_valid_ticket(ticket):
                yield ticket

    def map_fields_to_positions(self, tickets: list[tuple[int]]) -> dict[str, int]:
        num_fields = len(self.field_validators)
        correspondence_matrix = _CorrespondenceMatrix(num_fields)
        for ticket in self._valid_tickets(tickets):
            for position, value in enumerate(ticket):
                for field_idx, field_validator in enumerate(self.field_validators):
                    if not field_validator.is_valid(value):
                        correspondence_matrix.set_correspondence(
                            position,
                            field_idx,
                            _CorrespondenceStatus.DOES_NOT_CORRESPOND,
                        )

        correspondences = dict()
        for position, field_idx in correspondence_matrix.cells_which_correspond():
            correspondences[self.field_validators[field_idx].field_name] = position
        return correspondences
