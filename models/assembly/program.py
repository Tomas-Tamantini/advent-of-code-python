from typing import Protocol, Optional
from .instruction import Instruction


class Program(Protocol):
    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        ...
