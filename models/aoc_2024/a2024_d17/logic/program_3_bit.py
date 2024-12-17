from typing import Optional

from models.common.assembly.instruction import Instruction

from .parse_instructions_3_bit import parse_3_bit_instruction


class Program3Bit:
    def __init__(self, instructions: tuple[int, ...]):
        self._instructions = instructions

    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        if program_counter < 0 or program_counter >= len(self._instructions):
            return None
        else:
            return parse_3_bit_instruction(
                self._instructions[program_counter],
                self._instructions[program_counter + 1],
            )
