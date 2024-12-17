class SerialOutput3Bit:
    def __init__(self):
        self._output_values = []

    def write(self, value: int) -> None:
        self._output_values.append(value)

    def get_output(self) -> str:
        return ",".join(map(str, self._output_values))
