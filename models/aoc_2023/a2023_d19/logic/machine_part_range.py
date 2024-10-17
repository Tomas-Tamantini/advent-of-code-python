from typing import Iterator
from math import prod
from models.common.number_theory.interval import Interval


class MachinePartRange:
    def __init__(self, attributes: dict[chr, Interval]):
        self._attributes = attributes

    def attributes(self) -> Iterator[chr]:
        return iter(self._attributes.keys())

    def interval(self, attribute: chr) -> Interval:
        return self._attributes[attribute]

    def num_parts(self) -> int:
        return prod(
            max(attribute.num_elements, 0) for attribute in self._attributes.values()
        )

    def rating_sum(self) -> int:
        return sum(attribute.min_inclusive for attribute in self._attributes.values())

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, MachinePartRange):
            return False
        return self._attributes == value._attributes
