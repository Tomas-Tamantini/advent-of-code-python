from dataclasses import dataclass

from .part_number import PartNumber


@dataclass(frozen=True)
class EngineSymbol:
    symbol_chr: chr
    row: int
    column: int

    def is_adjacent_to(self, part_number: PartNumber) -> bool:
        if abs(part_number.row - self.row) > 1:
            return False
        if (part_number.start_column - self.column) > 1:
            return False
        if (self.column - part_number.end_column) > 1:
            return False
        return True
