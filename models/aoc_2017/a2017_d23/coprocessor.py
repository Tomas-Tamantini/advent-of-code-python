from dataclasses import dataclass

from models.common.assembly import (
    Computer,
    Hardware,
    ImmutableProgram,
    Instruction,
    Processor,
    UpdateRegisterInstruction,
)
from models.common.number_theory import is_prime


@dataclass(frozen=True)
class SpyMultiplyInstruction(UpdateRegisterInstruction):
    @staticmethod
    def _updated_value(value_source: int, value_destination: int) -> int:
        return value_source * value_destination

    def execute(self, hardware: Hardware) -> None:
        hardware.serial_output.write(1)
        return super().execute(hardware)


class InstructionCounter:
    def __init__(self):
        self._count = 0

    @property
    def count(self):
        return self._count

    def write(self, value: int) -> None:
        self._count += value


def count_multiply_instructions(instructions: list[Instruction]):
    instruction_counter = InstructionCounter()
    hardware = Hardware(
        processor=Processor(),
        serial_output=instruction_counter,
    )
    program = ImmutableProgram(instructions=instructions)
    computer = Computer(hardware=hardware)
    computer.run_program(program)
    return instruction_counter.count


def optimized_coprocessor_code(initial_a: int, initial_b: int):
    # Optimized assembly code by hand
    c = b = initial_b
    if initial_a != 0:
        b = b * 100 + 100_000
        c = b + 17_000
    h = 0
    for candidate in range(b, c + 1, 17):
        if not is_prime(candidate):
            h += 1
    return h
