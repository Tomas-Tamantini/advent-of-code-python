from dataclasses import dataclass

from .variable import VariableProtocol


@dataclass
class MilpSolution:
    variables: dict[VariableProtocol, float]
    objective_value: float
