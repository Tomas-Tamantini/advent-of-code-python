from typing import Protocol
from models.common.vectors import CardinalDirection
from .droid_input import DroidInput
from .droid_command import MoveCommand, TakeCommand


class DroidControl(Protocol):
    @property
    def droid_input(self) -> DroidInput: ...

    def handle_new_output_line(self, output_line: str) -> None: ...

    @property
    def airlock_password(self) -> str: ...


class DroidCLIControl:
    def __init__(self, droid_input: DroidInput) -> None:
        self._droid_input = droid_input
        self._airlock_password = None

    @property
    def airlock_password(self) -> str:
        if self._airlock_password is None:
            raise ValueError("Airlock password not set.")
        return self._airlock_password

    @property
    def droid_input(self) -> DroidInput:
        return self._droid_input

    def _prompt_input(self) -> None:
        command = input("Write command: ")
        self._droid_input.give_command(command)

    def handle_new_output_line(self, output_line: str) -> None:
        print(output_line)
        if "Command?" in output_line:
            self._prompt_input()
        elif "should be able to get in by typing" in output_line:
            self._airlock_password = int(output_line.split()[11])


# TODO: Implement actual exploration logic, rather than cheating by using pre-determined commands.
class DroidAutomaticControl:
    def __init__(self, droid_input: DroidInput) -> None:
        self._droid_input = droid_input
        self._airlock_password = None
        self._pre_determined_commands = [
            MoveCommand(CardinalDirection.EAST),
            TakeCommand("sand"),
            MoveCommand(CardinalDirection.WEST),
            MoveCommand(CardinalDirection.WEST),
            MoveCommand(CardinalDirection.NORTH),
            TakeCommand("wreath"),
            MoveCommand(CardinalDirection.EAST),
            TakeCommand("fixed point"),
            MoveCommand(CardinalDirection.WEST),
            MoveCommand(CardinalDirection.SOUTH),
            MoveCommand(CardinalDirection.SOUTH),
            MoveCommand(CardinalDirection.EAST),
            MoveCommand(CardinalDirection.EAST),
            MoveCommand(CardinalDirection.EAST),
            TakeCommand("space law space brochure"),
            MoveCommand(CardinalDirection.SOUTH),
            MoveCommand(CardinalDirection.SOUTH),
            MoveCommand(CardinalDirection.WEST),
        ]

    @property
    def airlock_password(self) -> str:
        if self._airlock_password is None:
            raise ValueError("Airlock password not set.")
        return self._airlock_password

    @property
    def droid_input(self) -> DroidInput:
        return self._droid_input

    def _give_next_input(self) -> None:
        next_command = self._pre_determined_commands.pop(0)
        self._droid_input.give_command(next_command)

    def handle_new_output_line(self, output_line: str) -> None:
        if "Command?" in output_line:
            self._give_next_input()
        elif "should be able to get in by typing" in output_line:
            self._airlock_password = int(output_line.split()[11])
