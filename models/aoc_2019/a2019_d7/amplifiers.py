from models.aoc_2019.intcode import IntcodeProgram
from models.common.assembly import Computer, Hardware, Processor


class AmplifierIO:
    class EmptyInput(Exception):
        pass

    class OutputWritten(Exception):
        pass

    def __init__(self, raise_error_on_write: bool = True) -> None:
        self._raise_error_on_write = raise_error_on_write
        self._values = []
        self._last_value_written = None

    @property
    def last_value_written(self) -> int:
        return self._last_value_written

    def silent_write(self, value: int) -> None:
        self._last_value_written = value
        self._values.append(value)

    def write(self, value: int) -> None:
        self.silent_write(value)
        if self._raise_error_on_write:
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
        self._halted = False

    @property
    def halted(self) -> bool:
        return self._halted

    def run_until_first_output(self) -> None:
        try:
            self._computer.run_program(self._program)
        except AmplifierIO.OutputWritten:
            return

    def run_until_halt_or_empty_input(self) -> None:
        while True:
            try:
                self._computer.run_next_instruction(self._program)
            except AmplifierIO.EmptyInput:
                return
            except StopIteration:
                self._halted = True
                return


class Amplifiers:
    def __init__(self, instructions: list[int]) -> None:
        self._instructions = instructions

    def run(self, phase_settings: list[int], input_signal: int) -> int:
        io_pipes = [
            AmplifierIO(raise_error_on_write=True)
            for _ in range(len(phase_settings) + 1)
        ]
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
            amplifier.run_until_first_output()
        return io_pipes[-1].last_value_written

    def run_with_feedback(self, phase_settings: list[int], input_signal: int) -> int:
        num_amplifiers = len(phase_settings)
        io_pipes = [
            AmplifierIO(raise_error_on_write=False) for _ in range(num_amplifiers)
        ]
        amplifiers = [
            _Amplifier(
                phase_setting=phase_setting,
                input_pipe=io_pipes[i],
                output_pipe=io_pipes[(i + 1) % num_amplifiers],
                instructions=self._instructions,
            )
            for i, phase_setting in enumerate(phase_settings)
        ]
        io_pipes[0].silent_write(input_signal)
        current_amplifier_idx = 0
        while not all(amplifier.halted for amplifier in amplifiers):
            amplifiers[current_amplifier_idx].run_until_halt_or_empty_input()
            current_amplifier_idx = (current_amplifier_idx + 1) % num_amplifiers
        return io_pipes[0].last_value_written
