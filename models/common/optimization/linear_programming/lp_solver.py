from typing import Iterator, Optional

import numpy as np
from scipy.optimize import linprog

from .constraint import Constraint, ConstraintType
from .lp_solution import MilpSolution
from .objective_function import ObjectiveFunction
from .variable import VariableProtocol


class MilpSolver:
    def __init__(self) -> None:
        self._variables = []
        self._constraints = []
        self._objective_function = None

    def add_variable(self, variable: VariableProtocol) -> None:
        self._variables.append(variable)

    def add_constraint(self, constraint: Constraint) -> None:
        self._constraints.append(constraint)

    def set_objective_function(self, objective_function: ObjectiveFunction) -> None:
        self._objective_function = objective_function

    def _objective_coefficients(self) -> np.ndarray:
        coefficients = np.zeros(len(self._variables))
        for i, variable in enumerate(self._variables):
            coefficient = self._objective_function.coefficient(variable.id)
            coefficients[i] = (
                coefficient
                if self._objective_function.is_minimization
                else -coefficient
            )
        return coefficients

    def _constraints_of_type(
        self, constraint_type: ConstraintType
    ) -> Iterator[Constraint]:
        return (c for c in self._constraints if c.constraint_type == constraint_type)

    def _inequality_matrix(self) -> Optional[np.ndarray]:
        matrix = []
        for constraint in self._constraints_of_type(ConstraintType.LESS_THAN_OR_EQUAL):
            coefficients = [
                constraint.coefficient(variable.id) for variable in self._variables
            ]
            matrix.append(coefficients)
        for constraint in self._constraints_of_type(
            ConstraintType.GREATER_THAN_OR_EQUAL
        ):
            coefficients = [
                -constraint.coefficient(variable.id) for variable in self._variables
            ]
            matrix.append(coefficients)
        return np.array(matrix) if matrix else None

    def _inequality_rhs(self) -> Optional[np.ndarray]:
        rhs = []
        for constraint in self._constraints_of_type(ConstraintType.LESS_THAN_OR_EQUAL):
            rhs.append(constraint.right_hand_side)
        for constraint in self._constraints_of_type(
            ConstraintType.GREATER_THAN_OR_EQUAL
        ):
            rhs.append(-constraint.right_hand_side)
        return np.array(rhs) if rhs else None

    def _equality_matrix(self) -> Optional[np.ndarray]:
        matrix = []
        for constraint in self._constraints_of_type(ConstraintType.EQUAL):
            coefficients = [
                constraint.coefficient(variable.id) for variable in self._variables
            ]
            matrix.append(coefficients)
        return np.array(matrix) if matrix else None

    def _equality_rhs(self) -> Optional[np.ndarray]:
        rhs = []
        for constraint in self._constraints_of_type(ConstraintType.EQUAL):
            rhs.append(constraint.right_hand_side)
        return np.array(rhs) if rhs else None

    def solve(self) -> MilpSolution:
        bounds = np.array(
            [
                (variable.lower_bound, variable.upper_bound)
                for variable in self._variables
            ]
        )
        integrality = np.array(
            [int(variable.is_integer) for variable in self._variables]
        )
        result = linprog(
            c=self._objective_coefficients(),
            A_ub=self._inequality_matrix(),
            b_ub=self._inequality_rhs(),
            A_eq=self._equality_matrix(),
            b_eq=self._equality_rhs(),
            bounds=bounds,
            method="highs",
            integrality=integrality,
        )
        if result.success is False:
            raise ValueError(result.message)
        variables = {
            variable: result.x[i] for i, variable in enumerate(self._variables)
        }
        objective_value = (
            result.fun if self._objective_function.is_minimization else -result.fun
        )
        return MilpSolution(variables, objective_value)
