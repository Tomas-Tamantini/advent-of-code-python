from .assembunny_parser import parse_assembunny_code
from .instructions import (
    AddAndMultiplyInstruction,
    DecrementInstruction,
    IncrementInstruction,
    ToggleInstruction,
)
from .program import AssembunnyProgram
from .self_referential_code import run_self_referential_code


__all__ = [
    "AddAndMultiplyInstruction",
    "AssembunnyProgram",
    "DecrementInstruction",
    "IncrementInstruction",
    "ToggleInstruction",
    "parse_assembunny_code",
    "run_self_referential_code",
]
