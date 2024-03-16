from typing import Iterator
from dataclasses import dataclass
from .vacuum_robot import VacuumRobotInstruction
from math import inf


@dataclass
class CompressedPath:
    main_routine: str
    subroutines: dict[str, str]

    @property
    def max_length(self) -> int:
        return max(
            len(self.main_routine),
            max(len(subroutine) for subroutine in self.subroutines.values()),
        )


@dataclass(frozen=True)
class _Interval:
    start_inclusive: int
    end_exclusive: int


class _SubroutineBuilder:
    def __init__(self, instructions: list[VacuumRobotInstruction]) -> None:
        self._instructions = instructions
        self._free_intervals = [_Interval(0, len(instructions))]


def _compress_path_recursive(
    builder: _SubroutineBuilder,
    num_subroutines: int,
) -> Iterator[CompressedPath]:
    if builder.is_complete():
        yield builder.compressed_path()
    elif num_subroutines >= 1:
        is_last = num_subroutines == 1
        max_size = builder.max_size_next_subroutine(is_last)
        for size in range(1, max_size + 1):
            new_builder = builder.add_subroutine(size)
            yield from _compress_path_recursive(new_builder, num_subroutines - 1)


def compress_vacuum_bot_path(
    instructions: list[VacuumRobotInstruction],
    num_subroutines: int,
) -> CompressedPath:
    best_path = None
    best_length = inf
    builder = _SubroutineBuilder(instructions)
    for path in _compress_path_recursive(builder, num_subroutines):
        if path.max_length < best_length:
            best_path = path
            best_length = path.max_length
    return best_path
