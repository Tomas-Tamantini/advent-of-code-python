from dataclasses import dataclass


@dataclass(frozen=True)
class PartNumber:
    serial: str
    row: int
    start_column: int

    @property
    def end_column(self) -> int:
        return self.start_column + len(self.serial) - 1

    @property
    def number(self) -> int:
        return int(self.serial)
