from dataclasses import dataclass
from typing import Iterator, Iterable


@dataclass(frozen=True)
class RobotInstruction:
    destination_id: int
    goes_to_output_bin: bool = False


@dataclass(frozen=True)
class RobotProgramming:
    instruction_low_id_chip: RobotInstruction
    instruction_high_id_chip: RobotInstruction


@dataclass(frozen=True)
class ChipAssignment:
    chip_id: int
    instruction: RobotInstruction


class ChipHandlerRobot:
    def __init__(self, program: RobotProgramming) -> None:
        self._chip_ids = []
        self._program = program

    def assign_chip(self, chip_id: int) -> None:
        if self.num_chips == 2:
            raise ValueError("Robot already has two chips")
        self._chip_ids.append(chip_id)

    def compared_chips(self, low_id: int, high_id: int) -> bool:
        return low_id in self._chip_ids and high_id in self._chip_ids

    @property
    def num_chips(self) -> int:
        return len(self._chip_ids)

    def chips_assignments(self) -> Iterator[ChipAssignment]:
        if self.num_chips != 2:
            raise ValueError("Not enough chips to follow instruction")
        yield ChipAssignment(
            chip_id=min(self._chip_ids),
            instruction=self._program.instruction_low_id_chip,
        )
        yield ChipAssignment(
            chip_id=max(self._chip_ids),
            instruction=self._program.instruction_high_id_chip,
        )


class ChipFactory:
    def __init__(
        self,
        input_assignments: Iterable[ChipAssignment],
        robot_programs: dict[int, RobotProgramming],
    ) -> None:
        self._robots = {
            robot_id: ChipHandlerRobot(program)
            for robot_id, program in robot_programs.items()
        }
        self._output_bins = dict()
        self._input_assignmens = input_assignments

    @property
    def output_bins(self) -> dict[int, list[int]]:
        return self._output_bins

    def _place_in_output_bin(self, chip_id: int, bin_id: int) -> None:
        self._output_bins.setdefault(bin_id, []).append(chip_id)

    def _assign_to_robot(self, chip_id: int, robot_id: int) -> None:
        robot = self._robots[robot_id]
        robot.assign_chip(chip_id)
        if robot.num_chips == 2:
            self._run_robot(robot)

    def _run_robot(self, robot: ChipHandlerRobot) -> None:
        for assignment in robot.chips_assignments():
            if assignment.instruction.goes_to_output_bin:
                self._place_in_output_bin(
                    chip_id=assignment.chip_id,
                    bin_id=assignment.instruction.destination_id,
                )
            else:
                self._assign_to_robot(
                    chip_id=assignment.chip_id,
                    robot_id=assignment.instruction.destination_id,
                )

    def run(self) -> None:
        for assignment in self._input_assignmens:
            robot = self._robots[assignment.instruction.destination_id]
            robot.assign_chip(assignment.chip_id)
            if robot.num_chips == 2:
                self._run_robot(robot)

    def robot_that_compared_chips(self, low_id: int, high_id: int) -> int:
        return next(
            (
                robot_id
                for robot_id, robot in self._robots.items()
                if robot.compared_chips(low_id, high_id)
            ),
            -1,
        )
