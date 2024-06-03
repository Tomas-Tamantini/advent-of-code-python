from typing import Iterator
from models.common.io import InputReader
from .bitmask_memory import (
    BitmaskInstruction,
    SetMaskInstruction,
    WriteToMemoryInstruction,
)


def _parse_bitmask_instruction(
    instruction: str, is_address_mask: bool
) -> BitmaskInstruction:
    parts = instruction.split(" = ")
    if "mask" in parts[0]:
        return SetMaskInstruction(parts[1], is_address_mask)
    else:
        return WriteToMemoryInstruction(
            address=int(parts[0].replace("mem[", "").replace("]", "")),
            value=int(parts[1]),
        )


def parse_bitmask_instructions(
    input_reader: InputReader, is_address_mask: bool
) -> Iterator[BitmaskInstruction]:
    for line in input_reader.read_stripped_lines():
        yield _parse_bitmask_instruction(line, is_address_mask)
