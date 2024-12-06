from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from models.common.optimization.branch_and_bound import maximize_with_branch_and_bound
from models.common.optimization.linear_programming import (
    BinaryVariable,
    Constraint,
    ConstraintType,
    ContinuousVariable,
    IntegerVariable,
    MilpSolver,
    ObjectiveFunction,
)


def test_continuous_variable_is_not_integer():
    variable = ContinuousVariable(id="x")
    assert not variable.is_integer


def test_integer_variable_is_integer():
    variable = IntegerVariable(id="x")
    assert variable.is_integer


def test_binary_variable_is_integer_with_two_possible_values():
    variable = BinaryVariable(id="x")
    assert variable.is_integer
    assert variable.lower_bound == 0
    assert variable.upper_bound == 1


def test_constraint_stores_coefficient_for_each_variable():
    constraint = Constraint(
        coefficients={"x": 1, "y": 2},
        right_hand_side=3,
        constraint_type=ConstraintType.EQUAL,
    )
    assert constraint.coefficient("x") == 1
    assert constraint.coefficient("y") == 2
    assert constraint.coefficient("z") == 0


def test_objective_function_stores_coefficient_for_each_variable():
    objective_function = ObjectiveFunction(
        coefficients={"x": 1, "y": 2},
        is_minimization=True,
    )
    assert objective_function.coefficient("x") == 1
    assert objective_function.coefficient("y") == 2
    assert objective_function.coefficient("z") == 0


def test_one_variable_milp_problem_gets_optimized():
    variable = ContinuousVariable(id="x", lower_bound=0, upper_bound=10)
    objective_function = ObjectiveFunction(
        coefficients={"x": 1},
        is_minimization=False,
    )
    constraint = Constraint(
        coefficients={"x": 1},
        right_hand_side=7,
        constraint_type=ConstraintType.LESS_THAN_OR_EQUAL,
    )
    solver = MilpSolver()
    solver.add_variable(variable)
    solver.set_objective_function(objective_function)
    solver.add_constraint(constraint)
    solution = solver.solve()
    assert len(solution.variables) == 1
    assert solution.variables[variable] == pytest.approx(7.0)
    assert solution.objective_value == pytest.approx(7.0)


def test_multi_variable_milp_problem_gets_optimized():
    var_x = ContinuousVariable(id="x", lower_bound=0, upper_bound=10)
    var_y = IntegerVariable(id="y", lower_bound=3, upper_bound=6)
    var_z = BinaryVariable(id="z")
    objective_function = ObjectiveFunction(
        coefficients={"x": 1, "y": 2, "z": 3},
        is_minimization=True,
    )
    constraint_1 = Constraint(
        coefficients={"x": 1, "y": 1},
        right_hand_side=7,
        constraint_type=ConstraintType.GREATER_THAN_OR_EQUAL,
    )
    constraint_2 = Constraint(
        coefficients={"y": 1, "z": 1},
        right_hand_side=5,
        constraint_type=ConstraintType.EQUAL,
    )
    solver = MilpSolver()
    solver.add_variable(var_x)
    solver.add_variable(var_y)
    solver.add_variable(var_z)
    solver.set_objective_function(objective_function)
    solver.add_constraint(constraint_1)
    solver.add_constraint(constraint_2)
    solution = solver.solve()
    assert len(solution.variables) == 3
    assert solution.variables[var_x] == pytest.approx(2.0)
    assert solution.variables[var_y] == pytest.approx(5.0)
    assert solution.variables[var_z] == pytest.approx(0.0)
    assert solution.objective_value == pytest.approx(12.0)


def test_unbounded_milp_problem_raises_exception():
    variable = ContinuousVariable(id="x", lower_bound=0)
    objective_function = ObjectiveFunction(
        coefficients={"x": 1},
        is_minimization=False,
    )
    solver = MilpSolver()
    solver.add_variable(variable)
    solver.set_objective_function(objective_function)
    with pytest.raises(ValueError):
        solver.solve()


def test_infeasible_milp_problem_raises_value_error():
    variable = ContinuousVariable(id="x", lower_bound=2, upper_bound=5)
    objective_function = ObjectiveFunction(
        coefficients={"x": 1},
        is_minimization=True,
    )
    constraint = Constraint(
        coefficients={"x": 1},
        right_hand_side=7,
        constraint_type=ConstraintType.GREATER_THAN_OR_EQUAL,
    )
    solver = MilpSolver()
    solver.add_variable(variable)
    solver.set_objective_function(objective_function)
    solver.add_constraint(constraint)
    with pytest.raises(ValueError):
        solver.solve()


def test_branch_and_bound_of_single_state_returns_that_state():
    mock_explorer = Mock()
    initial_state = "initial"
    mock_explorer.objective_value.return_value = 42
    mock_explorer.upper_bound_on_objective_value.return_value = 123
    mock_explorer.children_states.return_value = []
    result = maximize_with_branch_and_bound(initial_state, mock_explorer)
    assert result == 42


def test_branch_and_bound_finds_state_with_maximum_objective_value():
    initial_state = "A"
    mock_explorer = Mock()
    mock_explorer.objective_value.side_effect = ord
    mock_explorer.upper_bound_on_objective_value.side_effect = ord
    mock_explorer.children_states.side_effect = lambda state: ["B", "C"]
    result = maximize_with_branch_and_bound(initial_state, mock_explorer)
    assert result == ord("C")


def test_branch_and_bound_prunes_branches_with_insufficient_upper_bound():
    @dataclass
    class _StateSpy:
        value: int
        visited: bool = False
        children: list["_StateSpy"] = None

        def __hash__(self) -> int:
            return hash(self.value)

        def __eq__(self, other) -> bool:
            return self.value == other.value

    class MockExplorer:
        @staticmethod
        def objective_value(state):
            return state.value

        @staticmethod
        def upper_bound_on_objective_value(state):
            state.visited = True
            max_value = state.value
            for child in state.children or []:
                max_value = max(max_value, child.value)
            return max_value

        @staticmethod
        def children_states(state):
            return state.children or []

    state_a = _StateSpy(1)
    state_b = _StateSpy(2)
    state_c = _StateSpy(3)
    state_d = _StateSpy(5)
    state_e = _StateSpy(4)

    state_a.children = [state_c, state_b]
    state_b.children = [state_d]
    state_c.children = [state_e]

    result = maximize_with_branch_and_bound(state_a, MockExplorer())
    assert result == 5
    assert state_a.visited
    assert state_b.visited
    assert state_c.visited
    assert state_d.visited
    assert not state_e.visited
