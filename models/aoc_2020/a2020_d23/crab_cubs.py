from typing import Optional
from dataclasses import dataclass
from models.common.io import ProgressBar


@dataclass
class _CircularLinkedListNode:
    value: int
    next: Optional["_CircularLinkedListNode"] = None


class _CircularLinkedList:
    def __init__(self, values: list[int]) -> None:
        self._nodes = {value: _CircularLinkedListNode(value) for value in values}
        for i in range(len(values)):
            self._nodes[values[i]].next = self._nodes[values[(i + 1) % len(values)]]
        self.current = self._nodes[values[0]]

    def pop_after_current(self, num_nodes: int) -> list[_CircularLinkedListNode]:
        popped = []
        current_node = self.current
        for _ in range(num_nodes):
            current_node = current_node.next
            popped.append(current_node)
        self.current.next = current_node.next
        return popped

    def insert_segment_after_value(
        self, value: int, segment: list[_CircularLinkedListNode]
    ) -> None:
        destination_node = self.find(value)
        segment[-1].next = destination_node.next
        destination_node.next = segment[0]

    def find(self, value: int) -> _CircularLinkedListNode:
        return self._nodes[value]

    def as_list(self) -> list[int]:
        current_node = self.current
        values = [current_node.value]
        while (current_node := current_node.next) != self.current:
            values.append(current_node.value)
        return values


def _destination_value(
    current_value: int,
    forbidden_values: set[int],
    min_value: int,
    max_value: int,
):
    destination_value = current_value - 1
    while destination_value in forbidden_values or destination_value < min_value:
        destination_value -= 1
        if destination_value < min_value:
            destination_value = max_value
    return destination_value


def _crab_cups_iteration(
    cups: _CircularLinkedList, min_value: int, max_value: int
) -> None:
    current_node = cups.current
    picked_up = cups.pop_after_current(num_nodes=3)
    picked_up_values = {node.value for node in picked_up}
    destination_value = _destination_value(
        current_node.value, picked_up_values, min_value, max_value
    )
    cups.insert_segment_after_value(destination_value, picked_up)


def crab_cups(
    cups: list[int], num_moves: int, progress_bar: Optional[ProgressBar] = None
) -> list[int]:
    min_value, max_value = min(cups), max(cups)
    circular = _CircularLinkedList(cups)
    for i in range(num_moves):
        if progress_bar:
            progress_bar.update(i, num_moves)
        _crab_cups_iteration(circular, min_value, max_value)
        circular.current = circular.current.next
    return circular.as_list()
