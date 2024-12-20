from models.common.optimization.linear_programming import MilpSolver

from .blueprint import Blueprint
from .milp_model import constraints, objective_function, variables
from .mining_state import MiningState
from .resource_type import ResourceType


def max_num_resource(
    resource_to_maximize: ResourceType,
    time_limit: int,
    blueprint: Blueprint,
    initial_state: MiningState,
) -> int:
    solver = MilpSolver()
    for variable in variables(time_limit):
        solver.add_variable(variable)
    obj_fun = objective_function(resource_to_maximize, time_limit)
    solver.set_objective_function(obj_fun)
    for constraint in constraints(time_limit, blueprint, initial_state):
        solver.add_constraint(constraint)
    solution = solver.solve()
    return round(solution.objective_value)
