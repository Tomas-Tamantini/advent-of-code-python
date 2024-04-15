from dataclasses import dataclass
from models.assembly import Hardware


@dataclass(frozen=True)
class IncrementGlobalAccumulatorInstruction:
    increment: int

    def execute(self, hardware: Hardware) -> None:
        hardware.global_accumulator += self.increment
        hardware.increment_program_counter(1)


@dataclass(frozen=True)
class JumpOrNoOpInstruction:
    offset: int
    is_jump: bool = True

    def execute(self, hardware: Hardware) -> None:
        if self.is_jump:
            hardware.increment_program_counter(self.offset)
        else:
            hardware.increment_program_counter(1)

    def toggle(self) -> "JumpOrNoOpInstruction":
        return JumpOrNoOpInstruction(offset=self.offset, is_jump=not self.is_jump)
