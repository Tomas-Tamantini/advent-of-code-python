from dataclasses import dataclass
from models.assembly import UpdateRegisterInstruction
from models.assembly import Hardware, Instruction, Processor, Computer, ImmutableProgram


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
