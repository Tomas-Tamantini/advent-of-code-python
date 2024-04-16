from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class RangeInterval:
    min_inclusive: int
    max_inclusive: int

    def contains(self, number: int) -> bool:
        return self.min_inclusive <= number <= self.max_inclusive


@dataclass(frozen=True)
class TicketFieldValidator:
    field_name: str
    intervals: tuple[RangeInterval, ...]

    def is_valid(self, value: int) -> bool:
        return any(interval.contains(value) for interval in self.intervals)


@dataclass(frozen=True)
class TicketValidator:
    field_validators: tuple[TicketFieldValidator, ...]

    def is_valid_field(self, value: int) -> bool:
        return any(
            field_validator.is_valid(value) for field_validator in self.field_validators
        )
