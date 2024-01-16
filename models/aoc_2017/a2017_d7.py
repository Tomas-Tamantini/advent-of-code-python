from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    name: str
    parent: Optional["TreeNode"]
    children: list["TreeNode"]


class TreeBuilder:
    def __init__(self) -> None:
        self._nodes = {}

    def add_node(self, name: str, children: list[str] = None) -> None:
        if children is None:
            children = []
        new_node = self._nodes.get(name, TreeNode(name, None, []))
        children_nodes = []
        for child in children:
            if child in self._nodes:
                self._nodes[child].parent = new_node
            else:
                self._nodes[child] = TreeNode(child, new_node, [])
            children_nodes.append(self._nodes[child])
        new_node.children = children_nodes
        if name not in self._nodes:
            self._nodes[name] = new_node

    def root(self) -> Optional[TreeNode]:
        if not self._nodes:
            return None
        node = next(iter(self._nodes.values()))
        while node.parent is not None:
            node = node.parent
        return node
