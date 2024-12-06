from dataclasses import dataclass

from .variable import VariableId


@dataclass
class ObjectiveFunction:
    coefficients: dict[VariableId, float]
    is_minimization: bool

    def coefficient(self, variable_id: VariableId) -> float:
        return self.coefficients.get(variable_id, 0.0)
