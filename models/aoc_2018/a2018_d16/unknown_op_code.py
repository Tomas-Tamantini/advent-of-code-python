from dataclasses import dataclass
from typing import Iterator
from models.common.assembly import Hardware, Processor
from models.aoc_2018.three_value_instructions import ThreeValueInstruction


@dataclass(frozen=True)
class InstructionSample:
    op_code: int
    instruction_values: tuple[int, int, int]
    registers_before: tuple[int, ...]
    registers_after: tuple[int, ...]


def _instruction_matches_result(
    instruction: ThreeValueInstruction,
    instruction_sample: InstructionSample,
) -> bool:
    num_registers = len(instruction_sample.registers_before)
    if any(r < 0 or r >= num_registers for r in instruction.registers_used()):
        return False
    processor = Processor(
        registers=dict(enumerate(instruction_sample.registers_before))
    )
    hardware = Hardware(processor)
    instruction.execute(hardware)
    return processor.registers == dict(enumerate(instruction_sample.registers_after))


def possible_instructions(
    instruction_sample: InstructionSample,
    candidates: list[type[ThreeValueInstruction]],
) -> Iterator[type[ThreeValueInstruction]]:
    for candidate in candidates:
        instruction = candidate(*instruction_sample.instruction_values)
        if _instruction_matches_result(instruction, instruction_sample):
            yield candidate


def work_out_op_codes(
    samples: list[InstructionSample],
    candidates: list[type[ThreeValueInstruction]],
) -> dict[int, type[ThreeValueInstruction]]:
    op_code_to_possible_instructions = _op_code_to_possible_instructions(
        samples, candidates
    )
    num_op_codes = len(op_code_to_possible_instructions)

    op_code_to_instruction = dict()
    while len(op_code_to_instruction) < num_op_codes:
        _disambiguate_next_instruction(
            op_code_to_possible_instructions,
            op_code_to_instruction,
        )

    return op_code_to_instruction


def _op_code_to_possible_instructions(
    samples: list[InstructionSample],
    candidates: list[type[ThreeValueInstruction]],
) -> dict[int, list[type[ThreeValueInstruction]]]:
    op_with_candidates = dict()
    for sample in samples:
        instruction_candidates = op_with_candidates.get(sample.op_code, candidates)
        reduced_candidates = list(possible_instructions(sample, instruction_candidates))
        op_with_candidates[sample.op_code] = reduced_candidates
    return op_with_candidates


def _disambiguate_next_instruction(
    op_code_to_possible_instructions: dict[int, list[type[ThreeValueInstruction]]],
    op_code_to_instruction: dict[int, type[ThreeValueInstruction]],
) -> None:
    instruction = None
    for op_code, possible_candidates in op_code_to_possible_instructions.items():
        if op_code in op_code_to_instruction or len(possible_candidates) > 1:
            continue
        if len(possible_candidates) == 0:
            raise ValueError(f"No candidates for op code {op_code}")
        instruction = possible_candidates[0]
        break

    if instruction is None:
        raise ValueError("Cannot determine any more op codes")

    op_code_to_instruction[op_code] = instruction
    del op_code_to_possible_instructions[op_code]
    for candidates in op_code_to_possible_instructions.values():
        if instruction in candidates:
            candidates.remove(instruction)
