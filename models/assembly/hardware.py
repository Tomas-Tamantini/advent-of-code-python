from typing import Optional, Hashable
from .processor import Processor
from .memory import Memory
from .serial_io import SerialInput, SerialOutput


class Hardware:
    def __init__(
        self,
        processor: Processor,
        memory: Optional[Memory] = None,
        serial_input: Optional[SerialInput] = None,
        serial_output: Optional[SerialOutput] = None,
        **kwargs,
    ) -> None:
        self._processor = processor
        self._memory = memory
        self._serial_input = serial_input
        self._serial_output = serial_output
        self.__dict__.update(kwargs)

    @property
    def processor(self) -> Processor:
        return self._processor

    @property
    def memory(self) -> Optional[Memory]:
        return self._memory

    @property
    def serial_input(self) -> Optional[SerialInput]:
        return self._serial_input

    @property
    def serial_output(self) -> Optional[SerialOutput]:
        return self._serial_output

    def get_value_at_register(self, register: Hashable) -> int:
        return self._processor.registers[register]

    def set_value_at_register(self, register: Hashable, value: int) -> None:
        self._processor.registers[register] = value

    def increment_value_at_register(self, register: Hashable, increment: int) -> None:
        self._processor.registers[register] += increment

    def increment_program_counter(self, increment: int = 1) -> None:
        self._processor.program_counter += increment
