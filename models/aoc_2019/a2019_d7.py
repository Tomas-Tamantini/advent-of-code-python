from .intcode import run_intcode_program, IntcodeProgram


class AmplifierSerialInput:
    def __init__(self) -> None:
        self._values = []

    def put(self, value: int) -> None:
        self._values.append(value)

    def read(self) -> int:
        return self._values.pop(0)


class AmplifierSerialOutput:
    def __init__(self) -> None:
        self._value = None

    def write(self, value: int) -> None:
        self._value = value
        raise StopIteration("Output written")

    def read(self) -> int:
        return self._value


class Amplifiers:
    def __init__(self, program: list[int]) -> None:
        self._program = program

    def run(self, phase_settings: list[int], input_signal: int) -> int:
        for phase_setting in phase_settings:
            serial_input = AmplifierSerialInput()
            serial_input.put(phase_setting)
            serial_input.put(input_signal)
            serial_output = AmplifierSerialOutput()
            program = IntcodeProgram(self._program.copy())
            run_intcode_program(
                program, serial_input=serial_input, serial_output=serial_output
            )
            input_signal = serial_output.read()
        return input_signal
