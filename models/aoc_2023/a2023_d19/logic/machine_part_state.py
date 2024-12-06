from dataclasses import dataclass

from .machine_part_range import MachinePartRange


@dataclass(frozen=True)
class MachinePartState:
    workflow_id: str
    part_range: MachinePartRange
