from dataclasses import dataclass
from enum import Enum
from typing import Iterator

from models.common.optimization.linear_programming import (
    BinaryVariable,
    ContinuousVariable,
    VariableProtocol,
)

from ..resource_type import ResourceType


class VariableClass(Enum):
    BUILD_DECISION = "x"
    RESOURCE_AMOUNT = "a"
    FLEET_SIZE = "f"


@dataclass(frozen=True)
class VariableId:
    variable_class: VariableClass
    resource_type: ResourceType
    minute: int


def variables(time_limit: int) -> Iterator[VariableProtocol]:
    for resource_type in ResourceType:
        for minute in range(1, time_limit + 2):
            yield BinaryVariable(
                id=VariableId(VariableClass.BUILD_DECISION, resource_type, minute),
                description=f"Robot type {resource_type} gets built on minute {minute}",
            )

            yield ContinuousVariable(
                id=VariableId(VariableClass.RESOURCE_AMOUNT, resource_type, minute),
                description=(
                    f"Amount of resource {resource_type} "
                    f"at the start of minute {minute}"
                ),
                lower_bound=0,
            )

            yield ContinuousVariable(
                id=VariableId(VariableClass.FLEET_SIZE, resource_type, minute),
                description=(
                    f"Fleet size of robot type {resource_type} "
                    f"at the start of minute {minute}"
                ),
                lower_bound=0,
            )
