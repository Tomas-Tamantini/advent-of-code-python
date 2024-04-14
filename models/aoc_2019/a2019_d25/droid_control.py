from typing import Protocol
from .droid_input import DroidInput


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


class DroidAutomaticControl:
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

    def handle_new_output_line(self, output_line: str) -> None:
        raise NotImplementedError("Automatic control not implemented yet.")
