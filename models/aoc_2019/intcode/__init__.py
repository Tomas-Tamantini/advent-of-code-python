from .instructions import (
    MemoryOrImmediate,
    IntcodeHalt,
    IntcodeAdd,
    IntcodeMultiply,
    IntcodeInput,
    IntcodeOutput,
)
from .instruction_parser import parse_next_instruction
from .program import IntcodeProgram
