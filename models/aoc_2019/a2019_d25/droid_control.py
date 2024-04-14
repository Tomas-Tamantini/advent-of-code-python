from .droid_input import DroidInput


class DroidCLIControl:
    def __init__(self, droid_input: DroidInput) -> None:
        self._droid_input = droid_input

    def _prompt_input(self) -> None:
        command = input("Write command: ")
        self._droid_input.give_command(command)

    def handle_new_output_line(self, output_line: str) -> None:
        print(output_line)
        if "Command?" in output_line:
            self._prompt_input()
