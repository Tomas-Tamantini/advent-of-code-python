from typing import Iterator

from .machine_part_range import MachinePartRange
from .machine_part_state import MachinePartState
from .workflow_rules import WorkflowRule


class Workflow:
    def __init__(
        self,
        workflow_id: str,
        rules: tuple[WorkflowRule, ...],
        default_next_workflow_id: str,
    ):
        self._workflow_id = workflow_id
        self._rules = rules
        self._default_next_workflow_id = default_next_workflow_id

    @property
    def workflow_id(self) -> str:
        return self._workflow_id

    def next_part_states(
        self, part_range: MachinePartRange
    ) -> Iterator[MachinePartState]:
        current_range = part_range
        for rule in self._rules:
            if current_range.num_parts() <= 0:
                break
            split_range = rule.split_range(current_range)
            match_range = split_range.match_range
            current_range = split_range.non_match_range
            if match_range.num_parts() > 0:
                yield MachinePartState(
                    workflow_id=rule.next_workflow_id, part_range=match_range
                )
        if current_range.num_parts() > 0:
            yield MachinePartState(
                workflow_id=self._default_next_workflow_id, part_range=current_range
            )
