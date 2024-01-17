from dataclasses import dataclass, field
from collections import defaultdict
from typing import Union


@dataclass
class Processor:
    registers: dict[chr, int] = field(default_factory=lambda: defaultdict(int))
    program_counter: int = 0

    def get_value(self, value: Union[chr, int]) -> int:
        return value if isinstance(value, int) else self.registers[value]
