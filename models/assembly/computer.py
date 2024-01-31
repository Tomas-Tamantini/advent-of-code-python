from .processor import Processor
from .hardware import Hardware
from .program import Program


class Computer:
    def __init__(self, hardware: Hardware) -> None:
        self._hardware = hardware

    @classmethod
    def from_processor(cls, processor: Processor) -> "Computer":
        return cls(hardware=Hardware(processor=processor))

    def get_register_value(self, register: chr) -> int:
        return self._hardware.processor.get_value_or_immediate(register)

    @property
    def _program_counter(self) -> int:
        return self._hardware.processor.program_counter

    def run_next_instruction(self, program: Program) -> None:
        instruction = program.get_instruction(self._program_counter)
        if instruction is None:
            raise StopIteration("No more instructions to run")
        instruction.execute(hardware=self._hardware)

    def run_program(self, program: Program) -> None:
        while True:
            try:
                self.run_next_instruction(program)
            except StopIteration:
                break
