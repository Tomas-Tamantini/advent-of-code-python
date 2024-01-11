from typing import Iterable


class MessageReconstructor:
    def __init__(self, received_messages: Iterable[str]) -> None:
        self._received_messages = received_messages

    def reconstruct_message(self) -> str:
        return "".join(
            max(set(column), key=column.count)
            for column in zip(*self._received_messages)
        )
