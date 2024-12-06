from typing import Optional

from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program


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
    instructions: list[int], air_conditioner_id: int
) -> int:
    program = IntcodeProgram(instructions[:])
    serial_input = AirConditionerSerialInput(air_conditioner_id)
    serial_output = AirConditionerSerialOutput()
    run_intcode_program(program, serial_input=serial_input, serial_output=serial_output)
    return serial_output.peek()
