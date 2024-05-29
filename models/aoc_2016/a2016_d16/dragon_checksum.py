class DragonChecksum:
    def __init__(self, disk_space: int) -> None:
        self._disk_space = disk_space

    @staticmethod
    def dragon_curve(input: str) -> str:
        return input + "0" + "".join("1" if c == "0" else "0" for c in reversed(input))

    @staticmethod
    def _checksum_iterations(input: str) -> str:
        return "".join(
            "1" if input[i] == input[i + 1] else "0" for i in range(0, len(input), 2)
        )

    def checksum(self, input: str) -> str:
        while len(input) < self._disk_space:
            input = self.dragon_curve(input)
        input = input[: self._disk_space]
        while len(input) % 2 == 0:
            input = self._checksum_iterations(input)
        return input
