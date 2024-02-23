from dataclasses import dataclass
from .vacuum_robot import VacuumRobotInstruction


@dataclass
class _CompressedPath:
    main_routine: str
    subroutines: dict[str, str]

    @property
    def max_length(self) -> int:
        return max(
            len(self.main_routine),
            max(len(subroutine) for subroutine in self.subroutines.values()),
        )


def compress_vacuum_bot_path(
    instructions: list[VacuumRobotInstruction],
    num_subroutines: int,
) -> _CompressedPath:
    raise NotImplementedError()
