from models.assembly import Hardware, Processor, Computer
from .intcode import IntcodeProgram


class AmplifierIO:
    class EmptyInput(Exception):
        pass

    class OutputWritten(Exception):
        pass

    def __init__(self) -> None:
        self._values = []

    def silent_write(self, value: int) -> None:
        self._values.append(value)

    def write(self, value: int) -> None:
        self._values.append(value)
        raise AmplifierIO.OutputWritten("Output written")

    def read(self) -> int:
        if not self._values:
            raise AmplifierIO.EmptyInput("No input to read")
        return self._values.pop(0)


class _Amplifier:
    def __init__(
        self,
        phase_setting: int,
        input_pipe: AmplifierIO,
        output_pipe: AmplifierIO,
        instructions: list[int],
    ) -> None:
        self._input = input_pipe
        self._output = output_pipe
        self._input.silent_write(phase_setting)
        self._program = IntcodeProgram(instructions.copy())
        self._computer = Computer(
            hardware=Hardware(
                processor=Processor(),
                memory=self._program,
                serial_input=self._input,
                serial_output=self._output,
            )
        )

    def _run_until_first_output(self) -> None:
        try:
            self._computer.run_program(self._program)
        except AmplifierIO.OutputWritten:
            return


class Amplifiers:
    def __init__(self, instructions: list[int]) -> None:
        self._instructions = instructions

    def run(self, phase_settings: list[int], input_signal: int) -> int:
        io_pipes = [AmplifierIO() for _ in range(len(phase_settings) + 1)]
        amplifiers = [
            _Amplifier(
                phase_setting=phase_setting,
                input_pipe=io_pipes[i],
                output_pipe=io_pipes[i + 1],
                instructions=self._instructions,
            )
            for i, phase_setting in enumerate(phase_settings)
        ]
        io_pipes[0].silent_write(input_signal)
        for amplifier in amplifiers:
            amplifier._run_until_first_output()
        return io_pipes[-1].read()

    def run_with_feedback(self, phase_settings: list[int], input_signal: int) -> int:
        raise NotImplementedError("Feedback mode not implemented yet")
