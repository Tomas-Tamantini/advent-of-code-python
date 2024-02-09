from typing import Optional
from models.assembly import Instruction
from .instruction_parser import parse_next_instruction


class IntcodeProgram:
    def __init__(self, sequence: list[int]) -> None:
        self._sequence = sequence

    @property
    def sequence(self) -> list[int]:
        return self._sequence

    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        if 0 <= program_counter < len(self._sequence):
            return parse_next_instruction(self._sequence[program_counter:])

    def read(self, address: int) -> int:
        return self._sequence[address]

    def write(self, address: int, new_value) -> None:
        self._sequence[address] = new_value
