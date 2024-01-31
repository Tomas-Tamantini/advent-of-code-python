from dataclasses import dataclass
from typing import Optional, Hashable
from .processor import Processor
from .memory import Memory
from .serial_io import SerialInput, SerialOutput


@dataclass
class Hardware:
    processor: Processor
    memory: Optional[Memory] = None
    serial_input: Optional[SerialInput] = None
    serial_output: Optional[SerialOutput] = None

    def get_value_at_register(self, register: Hashable) -> int:
        return self.processor.registers[register]

    def set_value_at_register(self, register: Hashable, value: int) -> None:
        self.processor.registers[register] = value

    def increment_value_at_register(self, register: Hashable, increment: int) -> None:
        self.processor.registers[register] += increment

    def increment_program_counter(self, increment: int = 1) -> None:
        self.processor.program_counter += increment
