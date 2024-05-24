from dataclasses import dataclass


@dataclass(frozen=True)
class InstructionWithDuration:
    value_increment: int
    num_cycles: int


class RegisterHistory:
    def __init__(self) -> None:
        self._history = [1]

    def run_instruction(self, instruction: InstructionWithDuration) -> None:
        self._history.extend([self._history[-1]] * (instruction.num_cycles - 1))
        new_value = self._history[-1] + instruction.value_increment
        self._history.append(new_value)

    def value_during_cycle(self, cycle: int) -> int:
        return (
            self._history[cycle - 1]
            if cycle <= len(self._history)
            else self._history[-1]
        )
