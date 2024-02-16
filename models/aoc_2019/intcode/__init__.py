from .instructions import (
    MemoryOrImmediate,
    IntcodeHalt,
    IntcodeAdd,
    IntcodeMultiply,
    IntcodeInput,
    IntcodeOutput,
    IntcodeJumpIfTrue,
    IntcodeJumpIfFalse,
    IntcodeLessThan,
    IntcodeEquals,
)
from .instruction_parser import parse_next_instruction
from .program import IntcodeProgram
from .run_program import run_intcode_program
