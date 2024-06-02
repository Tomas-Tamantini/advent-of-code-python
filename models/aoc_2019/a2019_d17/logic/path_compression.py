from typing import Iterator, Optional
from dataclasses import dataclass
from .vacuum_robot import VacuumRobotInstruction
from math import inf


@dataclass
class CompressedPath:
    main_routine: str
    subroutines: dict[str, str]

    def subroutines_in_order(self) -> Iterator[str]:
        accounted_for = set()
        for instruction in self.main_routine.split(","):
            if instruction in accounted_for:
                continue
            accounted_for.add(instruction)
            yield self.subroutines[instruction]

    @property
    def max_length(self) -> int:
        return max(
            len(self.main_routine),
            max(len(subroutine) for subroutine in self.subroutines.values()),
        )


@dataclass(frozen=True, order=True)
class _SubroutineInterval:
    start_inclusive: int
    end_exclusive: int
    subroutine_name: str

    @property
    def num_instructions(self) -> int:
        return self.end_exclusive - self.start_inclusive


class _SubroutineBuilder:
    def __init__(
        self,
        instructions: list[VacuumRobotInstruction],
        intervals: list[_SubroutineInterval] = None,
        subroutine_name: str = "A",
    ) -> None:
        self._instructions = instructions
        self._subroutine_intervals = intervals or []
        self._subroutine_name = subroutine_name

    def is_complete(self) -> bool:
        return len(self._instructions) == sum(
            interval.num_instructions for interval in self._subroutine_intervals
        )

    def _free_intervals(self) -> Iterator[tuple[int, int]]:
        free_idx_start = 0
        for interval in self._subroutine_intervals:
            if free_idx_start < interval.start_inclusive:
                yield (free_idx_start, interval.start_inclusive)
            free_idx_start = interval.end_exclusive
        if free_idx_start < len(self._instructions):
            yield (free_idx_start, len(self._instructions))

    def _next_free_interval(self) -> Optional[tuple[int, int]]:
        try:
            return next(self._free_intervals())
        except StopIteration:
            return None

    def _next_subroutine_name(self) -> str:
        return chr(ord(self._subroutine_name) + 1)

    def max_size_next_subroutine(self) -> int:
        if not self._subroutine_intervals:
            return len(self._instructions)
        next_interval = self._next_free_interval()
        if next_interval is None:
            return 0
        return next_interval[1] - next_interval[0]

    def add_subroutine(self, size: int) -> "_SubroutineBuilder":
        subroutine_instructions = self._instructions_new_subroutine(size)
        new_intervals = list(self._matches(subroutine_instructions))
        return _SubroutineBuilder(
            instructions=self._instructions,
            intervals=sorted(self._subroutine_intervals + new_intervals),
            subroutine_name=self._next_subroutine_name(),
        )

    def _instructions_new_subroutine(self, size: int) -> list[VacuumRobotInstruction]:
        first_free_interval = self._next_free_interval()
        if first_free_interval is None:
            raise ValueError("No free interval to add subroutine")
        return self._instructions[
            first_free_interval[0] : first_free_interval[0] + size
        ]

    def _matches(
        self, subroutine_instructions: list[VacuumRobotInstruction]
    ) -> Iterator[_SubroutineInterval]:
        size = len(subroutine_instructions)
        for free_interval_start, free_interval_end in self._free_intervals():
            i = free_interval_start
            while i + size <= free_interval_end:
                if self._instructions[i : i + size] == subroutine_instructions:
                    yield (_SubroutineInterval(i, i + size, self._subroutine_name))
                    i += size
                else:
                    i += 1

    def _defined_subroutine_names(self) -> set[str]:
        return {interval.subroutine_name for interval in self._subroutine_intervals}

    def _subroutine_instructions(
        self, subroutine_name: str
    ) -> list[VacuumRobotInstruction]:
        for interval in self._subroutine_intervals:
            if interval.subroutine_name == subroutine_name:
                return self._instructions[
                    interval.start_inclusive : interval.end_exclusive
                ]
        raise ValueError(f"Subroutine {subroutine_name} not found")

    def _instructions_to_str(self, instructions: list[VacuumRobotInstruction]) -> str:
        return ",".join(str(instruction) for instruction in instructions)

    def compressed_path(self) -> CompressedPath:
        subroutines = dict()
        for subroutine_name in self._defined_subroutine_names():
            instructions = self._subroutine_instructions(subroutine_name)
            subroutines[subroutine_name] = self._instructions_to_str(instructions)
        return CompressedPath(
            main_routine=self._main_routine_as_str(), subroutines=subroutines
        )

    def _main_routine_as_str(self):
        macro_instructions = [
            interval.subroutine_name for interval in sorted(self._subroutine_intervals)
        ]
        return ",".join(macro_instructions)


def _compress_path_recursive(
    builder: _SubroutineBuilder,
    num_subroutines: int,
) -> Iterator[CompressedPath]:
    if builder.is_complete():
        yield builder.compressed_path()
    elif num_subroutines >= 1:
        for size in range(1, builder.max_size_next_subroutine() + 1):
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
