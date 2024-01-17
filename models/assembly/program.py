from typing import Protocol, Optional
from .instruction import Instruction


class Program(Protocol):
    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        ...


class ImmutableProgram:
    def __init__(self, instructions: list[Instruction]):
        self._instructions = instructions

    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        return (
            self._instructions[program_counter]
            if 0 <= program_counter < len(self._instructions)
            else None
        )
