from typing import Iterable, Iterator

from .machine_part_range import MachinePartRange
from .machine_part_state import MachinePartState
from .workflow import Workflow


class WorkflowNetwork:
    def __init__(
        self,
        initial_workflow_id: str,
        accept_workflow_id: str,
        reject_workflow_id: str,
        workflows: Iterable[Workflow],
    ):
        self._initial_workflow_id = initial_workflow_id
        self._accept_workflow_id = accept_workflow_id
        self._reject_workflow_id = reject_workflow_id
        self._workflows = {w.workflow_id: w for w in workflows}

    def accepted_ranges(
        self, initial_range: MachinePartRange
    ) -> Iterator[MachinePartRange]:
        stack = [
            MachinePartState(
                workflow_id=self._initial_workflow_id, part_range=initial_range
            )
        ]
        while stack:
            state = stack.pop()
            if state.workflow_id == self._accept_workflow_id:
                if state.part_range.num_parts() > 0:
                    yield state.part_range
            elif state.workflow_id != self._reject_workflow_id:
                workflow = self._workflows[state.workflow_id]
                stack.extend(workflow.next_part_states(state.part_range))
