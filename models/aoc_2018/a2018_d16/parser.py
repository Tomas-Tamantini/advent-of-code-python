from typing import Iterator
from models.common.io import InputReader
from models.aoc_2018.three_value_instructions import ThreeValueInstruction
from .unknown_op_code import InstructionSample


def parse_instruction_samples(input_reader: InputReader) -> Iterator[InstructionSample]:
    lines = list(input_reader.readlines())
    for line_idx, line in enumerate(lines):
        if "Before" in line:
            lb = line.replace("[", "").replace("]", "").strip()
            lv = lines[line_idx + 1].strip()
            la = lines[line_idx + 2].replace("[", "").replace("]", "").strip()

            instruction_values = list(map(int, lv.split()))
            registers_before = tuple(map(int, lb.split(":")[1].split(",")))
            registers_after = tuple(map(int, la.split(":")[1].split(",")))

            yield InstructionSample(
                op_code=instruction_values[0],
                instruction_values=tuple(instruction_values[1:]),
                registers_before=registers_before,
                registers_after=registers_after,
            )


def parse_unknown_op_code_program(
    input_reader: InputReader,
    op_code_to_instruction: dict[int, type[ThreeValueInstruction]],
) -> Iterator[ThreeValueInstruction]:
    instructions = []
    for line in reversed(list(input_reader.readlines())):
        if "After:" in line:
            break
        if not line.strip():
            continue
        values = list(map(int, line.strip().split()))
        op_code = values[0]
        instruction_type = op_code_to_instruction[op_code]
        instructions.append(instruction_type(*values[1:]))
    yield from reversed(instructions)
