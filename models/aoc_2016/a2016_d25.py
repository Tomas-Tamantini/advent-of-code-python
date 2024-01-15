from .assembunny import Program, Computer, Processor


class ClockSignalSerialOutput:
    def __init__(self, buffer_size: int):
        self._buffer_size = buffer_size
        self._buffer = []
        self._expected_signal = 0

    def write(self, value: int) -> None:
        if value != self._expected_signal:
            raise ValueError(f"Expected signal {self._expected_signal}, got {value}")
        if len(self._buffer) >= self._buffer_size:
            raise OverflowError(f"Buffer overflow: {len(self._buffer)}")
        self._buffer.append(value)
        self._expected_signal = 1 - self._expected_signal


def smallest_value_to_send_clock_signal(program: Program) -> int:
    program.optimize()
    for guess in range(1_000):
        computer = Computer(
            processor=Processor(
                registers={"a": guess},
            ),
            serial_output=ClockSignalSerialOutput(buffer_size=20),
        )
        try:
            computer.run(program, optimize_assembunny_code=False)
        except ValueError:
            continue
        except OverflowError:
            return guess
    raise ValueError("No solution found")
