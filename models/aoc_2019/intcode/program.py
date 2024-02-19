from typing import Optional
from models.assembly import Instruction
from .instruction_parser import parse_next_instruction


class IntcodeProgram:
    def __init__(self, instructions: list[int]) -> None:
        self._instructions = instructions

    @property
    def instructions(self) -> list[int]:
        return self._instructions

    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        if 0 <= program_counter < len(self._instructions):
            return parse_next_instruction(self._instructions[program_counter:])

    def read(self, address: int) -> int:
        return self._instructions[address]

    def write(self, address: int, new_value) -> None:
        self._instructions[address] = new_value
