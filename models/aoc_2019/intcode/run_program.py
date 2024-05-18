from typing import Optional
from models.common.assembly import (
    Hardware,
    Processor,
    Computer,
    SerialInput,
    SerialOutput,
)
from .program import IntcodeProgram


def run_intcode_program(
    program: IntcodeProgram,
    processor: Optional[Processor] = None,
    serial_input: Optional[SerialInput] = None,
    serial_output: Optional[SerialOutput] = None,
) -> None:
    if processor is None:
        processor = Processor()
    hardware = Hardware(
        processor=processor,
        memory=program,
        serial_input=serial_input,
        serial_output=serial_output,
        relative_base=0,
    )
    computer = Computer(hardware)
    computer.run_program(program)
