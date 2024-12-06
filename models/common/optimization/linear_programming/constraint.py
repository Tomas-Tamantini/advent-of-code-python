from dataclasses import dataclass
from enum import Enum

from .variable import VariableId


class ConstraintType(Enum):
    LESS_THAN_OR_EQUAL = 1
    EQUAL = 2
    GREATER_THAN_OR_EQUAL = 3


@dataclass
class Constraint:
    coefficients: dict[VariableId, float]
    right_hand_side: float
    constraint_type: ConstraintType
    description: str = ""

    def coefficient(self, variable_id: VariableId) -> float:
        return self.coefficients.get(variable_id, 0)
