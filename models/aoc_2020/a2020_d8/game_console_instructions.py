from dataclasses import dataclass
from models.assembly import Hardware


@dataclass(frozen=True)
class IncrementGlobalAccumulatorInstruction:
    increment: int

    def execute(self, hardware: Hardware) -> None:
        hardware.global_accumulator += self.increment
        hardware.increment_program_counter(1)


@dataclass(frozen=True)
class UnconditionalJumpInstruction:
    offset: int

    def execute(self, hardware: Hardware) -> None:
        hardware.increment_program_counter(self.offset)
