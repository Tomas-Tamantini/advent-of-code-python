from dataclasses import dataclass
from typing import Iterator, Optional
from models.common.io import ProgressBar


@dataclass
class _CircularListNode:
    value: int
    next_node: "_CircularListNode"
    previous_node: "_CircularListNode"


class _CircularLinkedList:
    def __init__(self, nodes: list[_CircularListNode]) -> None:
        self._nodes = nodes

    @property
    def nodes(self) -> list[_CircularListNode]:
        return self._nodes

    def values_in_order(self) -> Iterator[int]:
        current_node = self.nodes[0]
        for _ in range(len(self.nodes)):
            yield current_node.value
            current_node = current_node.next_node

    def remove_node(self, node: _CircularListNode) -> None:
        node.previous_node.next_node = node.next_node
        node.next_node.previous_node = node.previous_node

    def move_node(self, node: _CircularListNode, num_steps: int) -> None:
        position_to_insert = node.previous_node
        self.remove_node(node)
        reduced_steps = num_steps % (len(self._nodes) - 1)
        for _ in range(reduced_steps):
            position_to_insert = position_to_insert.next_node
        self.add_node_after(node, position_to_insert)

    def add_node_after(
        self, node_to_insert: _CircularListNode, position_to_insert: _CircularListNode
    ) -> None:
        node_to_insert.next_node = position_to_insert.next_node
        node_to_insert.previous_node = position_to_insert
        position_to_insert.next_node = node_to_insert
        node_to_insert.next_node.previous_node = node_to_insert


def _initialize_linked_list(lst: list[int]) -> _CircularLinkedList:
    nodes = [_CircularListNode(value, None, None) for value in lst]
    for i, node in enumerate(nodes):
        node.next_node = nodes[(i + 1) % len(nodes)]
        node.previous_node = nodes[(i - 1) % len(nodes)]
    linked_list = _CircularLinkedList(nodes)
    return linked_list


def _shuffle_list_once(linked_list: _CircularLinkedList) -> None:
    for node in linked_list.nodes:
        linked_list.move_node(node, num_steps=node.value)


def mix_list(
    lst: list[int], num_rounds: int = 1, progress_bar: Optional[ProgressBar] = None
) -> list[int]:
    linked_list = _initialize_linked_list(lst)
    for r in range(num_rounds):
        if progress_bar:
            progress_bar.update(r, num_rounds)
        _shuffle_list_once(linked_list)
    return list(linked_list.values_in_order())
