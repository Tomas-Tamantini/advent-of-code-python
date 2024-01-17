from dataclasses import dataclass
from enum import Enum
from typing import Iterator
from models.assembly import Hardware, ImmutableProgram, Processor, Computer


class ComparisonOperator(Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="


@dataclass(frozen=True)
class ConditionalIncrementInstruction:
    register_to_increment: str
    increment_amount: int
    comparison_register: str
    value_to_compare: int
    comparison_operator: ComparisonOperator

    def _comparison_is_met(self, register_value: int) -> bool:
        if self.comparison_operator == ComparisonOperator.EQUALS:
            return register_value == self.value_to_compare
        elif self.comparison_operator == ComparisonOperator.NOT_EQUALS:
            return register_value != self.value_to_compare
        elif self.comparison_operator == ComparisonOperator.GREATER_THAN:
            return register_value > self.value_to_compare
        elif self.comparison_operator == ComparisonOperator.GREATER_THAN_OR_EQUAL:
            return register_value >= self.value_to_compare
        elif self.comparison_operator == ComparisonOperator.LESS_THAN:
            return register_value < self.value_to_compare
        elif self.comparison_operator == ComparisonOperator.LESS_THAN_OR_EQUAL:
            return register_value <= self.value_to_compare
        else:
            raise ValueError(f"Unknown comparison operator: {self.comparison_operator}")

    def execute(self, hardware: Hardware) -> None:
        if self._comparison_is_met(
            hardware.get_value_at_register(self.comparison_register)
        ):
            hardware.increment_value_at_register(
                self.register_to_increment,
                self.increment_amount,
            )
        hardware.increment_program_counter()


def maximum_value_at_registers(
    instructions: list[ConditionalIncrementInstruction],
) -> Iterator[int]:
    program = ImmutableProgram(instructions)
    processor = Processor()
    computer = Computer.from_processor(processor)
    while True:
        yield max(processor.registers.values()) if processor.registers else 0
        try:
            computer.run_next_instruction(program)
        except StopIteration:
            break
