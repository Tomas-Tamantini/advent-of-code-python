from models.common.optimization.linear_programming import ObjectiveFunction
from ..resource_type import ResourceType
from .variables import VariableClass, VariableId


def objective_function(
    resource_to_maximize: ResourceType, time_limit: int
) -> ObjectiveFunction:
    var_id = VariableId(
        VariableClass.RESOURCE_AMOUNT, resource_to_maximize, time_limit + 1
    )
    obj_coeff = {var_id: 1}
    return ObjectiveFunction(obj_coeff, is_minimization=False)
