from enum import Enum


class MatchType(Enum):
    EXACT = 1
    GREATER_THAN = 2
    LESS_THAN = 3


class AuntSue:
    def __init__(self, id: int, attributes: dict[str, int]) -> None:
        self._id = id
        self._attributes = attributes

    @property
    def id(self) -> int:
        return self._id

    @staticmethod
    def _attribute_matches(
        attribute_value: int, other_attribute_value: int, match_type: MatchType
    ) -> bool:
        if match_type == MatchType.EXACT:
            return attribute_value == other_attribute_value
        elif match_type == MatchType.GREATER_THAN:
            return attribute_value > other_attribute_value
        else:
            return attribute_value < other_attribute_value

    def matches(self, other_attributes: dict[str, tuple[int, MatchType]]) -> bool:
        for attribute, value in self._attributes.items():
            if not self._attribute_matches(value, *other_attributes[attribute]):
                return False
        return True
