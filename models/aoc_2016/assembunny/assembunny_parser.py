from models.common.io import InputReader
from models.common.assembly import (
    CopyInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
)
from .instructions import (
    DecrementInstruction,
    IncrementInstruction,
    ToggleInstruction,
)
from .program import AssembunnyProgram


def _parse_assembunny_instruction(line: str):
    raw_parts = line.split(" ")
    parts = []
    for part in raw_parts[1:]:
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(part)
    if "cpy" in line:
        return CopyInstruction(source=parts[0], destination=parts[1])
    elif "inc" in line:
        return IncrementInstruction(register=parts[0])
    elif "dec" in line:
        return DecrementInstruction(register=parts[0])
    elif "jnz" in line:
        return JumpNotZeroInstruction(
            value_to_compare=parts[0],
            offset=parts[1],
        )
    elif "tgl" in line:
        return ToggleInstruction(offset=parts[0])
    elif "out" in line:
        return OutInstruction(source=parts[0])
    else:
        raise ValueError(f"Unknown instruction: {line.strip()}")


def parse_assembunny_code(input_reader: InputReader) -> AssembunnyProgram:
    instructions = [
        _parse_assembunny_instruction(line)
        for line in input_reader.read_stripped_lines()
    ]
    return AssembunnyProgram(instructions)
