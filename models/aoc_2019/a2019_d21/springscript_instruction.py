from dataclasses import dataclass
from enum import Enum


class SpringScriptInstructionType(str, Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclass(frozen=True)
class SpringScriptInstruction:
    instruction_type: SpringScriptInstructionType
    register_a: str
    register_b: str

    def __str__(self) -> str:
        return f"{self.instruction_type.value} {self.register_a} {self.register_b}"
