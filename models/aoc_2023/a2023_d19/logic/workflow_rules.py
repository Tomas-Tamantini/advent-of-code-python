from typing import Protocol
from dataclasses import dataclass
from models.common.number_theory.interval import Interval
from .machine_part_range import MachinePartRange
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class SplitRange:
    match_range: MachinePartRange
    non_match_range: MachinePartRange


class WorkflowRule(Protocol):
    def split_range(self, part_range: MachinePartRange) -> SplitRange: ...


@dataclass(frozen=True)
class _InequalityRule(ABC):
    attribute_name: str
    threshold: int
    next_workflow_id: str

    @abstractmethod
    def _match_interval(self, original_interval: Interval) -> Interval: ...

    @abstractmethod
    def _remaining_interval(self, original_interval: Interval) -> Interval: ...

    def split_range(self, part_range: MachinePartRange) -> SplitRange:
        match_attributes = dict()
        non_match_attributes = dict()
        for attribute in part_range.attributes():
            original_interval = part_range.interval(attribute)
            if attribute == self.attribute_name:
                match_attributes[attribute] = self._match_interval(original_interval)
                non_match_attributes[attribute] = self._remaining_interval(
                    original_interval
                )
            else:
                match_attributes[attribute] = original_interval
                non_match_attributes[attribute] = original_interval
        return SplitRange(
            match_range=MachinePartRange(match_attributes),
            non_match_range=MachinePartRange(non_match_attributes),
        )


class LessThanRule(_InequalityRule):
    def _match_interval(self, original_interval: Interval) -> Interval:
        return Interval(
            min_inclusive=original_interval.min_inclusive,
            max_inclusive=min(original_interval.max_inclusive, self.threshold - 1),
        )

    def _remaining_interval(self, original_interval: Interval) -> Interval:
        return Interval(
            min_inclusive=max(original_interval.min_inclusive, self.threshold),
            max_inclusive=original_interval.max_inclusive,
        )


class GreaterThanRule(_InequalityRule):
    def _match_interval(self, original_interval: Interval) -> Interval:
        return Interval(
            min_inclusive=max(original_interval.min_inclusive, self.threshold + 1),
            max_inclusive=original_interval.max_inclusive,
        )

    def _remaining_interval(self, original_interval: Interval) -> Interval:
        return Interval(
            min_inclusive=original_interval.min_inclusive,
            max_inclusive=min(original_interval.max_inclusive, self.threshold),
        )
