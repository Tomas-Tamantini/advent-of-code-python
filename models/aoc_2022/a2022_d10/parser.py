from typing import Iterator

from models.common.io import InputReader

from .logic import InstructionWithDuration


def parse_instructions_with_duration(
    input_reader: InputReader,
) -> Iterator[InstructionWithDuration]:
    for line in input_reader.read_stripped_lines():
        if "noop" in line:
            yield InstructionWithDuration(value_increment=0, num_cycles=1)
        else:
            yield InstructionWithDuration(
                value_increment=int(line.split()[1]), num_cycles=2
            )
