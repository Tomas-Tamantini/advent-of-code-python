from typing import Iterator
from models.common.io import InputReader
from .conditional_increment import ConditionalIncrementInstruction, ComparisonOperator


def _parse_conditional_increment_instruction(
    line: str,
) -> ConditionalIncrementInstruction:
    parts = line.strip().split(" ")
    increment_amount = int(parts[2])
    if "dec" in parts[1]:
        increment_amount = -increment_amount
    return ConditionalIncrementInstruction(
        register_to_increment=parts[0],
        increment_amount=increment_amount,
        comparison_register=parts[4],
        value_to_compare=int(parts[6]),
        comparison_operator=ComparisonOperator(parts[5]),
    )


def parse_conditional_increment_instructions(
    input_reader: InputReader,
) -> Iterator[ConditionalIncrementInstruction]:
    for line in input_reader.readlines():
        yield _parse_conditional_increment_instruction(line)
