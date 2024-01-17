from typing import Optional
from models.assembly import Processor, SerialOutput
from .program import Program


class Computer:
    def __init__(
        self,
        processor: Processor,
        serial_output: Optional[SerialOutput] = None,
    ) -> None:
        self._processor = processor
        self._serial_output = serial_output

    def run(self, program: Program, optimize_assembunny_code: bool):
        if optimize_assembunny_code:
            program.optimize()
        while True:
            instruction = program.get_instruction(self._processor.program_counter)
            if instruction is None:
                return
            instruction.execute(
                processor=self._processor,
                memory=program,
                serial_output=self._serial_output,
            )

    def value_at(self, register: chr) -> int:
        return self._processor.registers[register]
