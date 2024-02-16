from typing import Optional
from models.assembly import Hardware, Computer, Processor
from .intcode import IntcodeProgram


class AirConditionerSerialInput:
    def __init__(self, air_conditioner_id: int) -> None:
        self._air_conditioner_id = air_conditioner_id

    def read(self) -> int:
        return self._air_conditioner_id


class AirConditionerSerialOutput:
    def __init__(self) -> None:
        self._output_values = []

    def peek(self) -> Optional[int]:
        if self._output_values:
            return self._output_values[-1]
        return None

    def write(self, value: int) -> None:
        self._output_values.append(value)


def run_air_conditioner_program(
    sequence: list[int],
    serial_input: AirConditionerSerialInput,
    serial_output: AirConditionerSerialOutput,
) -> None:
    program = IntcodeProgram(sequence[:])
    hardware = Hardware(
        processor=Processor(),
        memory=program,
        serial_input=serial_input,
        serial_output=serial_output,
    )
    computer = Computer(hardware)
    computer.run_program(program)
