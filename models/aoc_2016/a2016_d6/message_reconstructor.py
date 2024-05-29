from typing import Iterable


class MessageReconstructor:
    def __init__(self, received_messages: Iterable[str]) -> None:
        self._received_messages = received_messages

    def _columns(self) -> Iterable[str]:
        return zip(*self._received_messages)

    def reconstruct_message_from_most_common_chars(self) -> str:
        return "".join(max(set(column), key=column.count) for column in self._columns())

    def reconstruct_message_from_least_common_chars(self) -> str:
        return "".join(min(set(column), key=column.count) for column in self._columns())
