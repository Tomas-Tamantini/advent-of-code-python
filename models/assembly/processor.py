from dataclasses import dataclass, field
from collections import defaultdict
from typing import Hashable


@dataclass
class Processor:
    registers: dict[Hashable, int] = field(default_factory=lambda: defaultdict(int))
    program_counter: int = 0

    def get_value_or_immediate(self, value: Hashable) -> int:
        return value if isinstance(value, int) else self.registers[value]
