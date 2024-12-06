from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class _WeightImbalance:
    node: str
    actual_weight: int
    expected_weight: int


@dataclass
class TreeNode:
    name: str
    weight: int
    parent: Optional["TreeNode"]
    children: list["TreeNode"]

    def total_weight(self) -> int:
        return self.weight + sum(child.total_weight() for child in self.children)

    def _imbalanced_child(self) -> Optional[_WeightImbalance]:
        children_by_weight = defaultdict(list)
        for child in self.children:
            children_by_weight[child.total_weight()].append(child)
        typical_weight = -1
        max_count = -1
        for weight, children in children_by_weight.items():
            if len(children) > max_count:
                typical_weight = weight
                max_count = len(children)
        for child in self.children:
            if child.total_weight() != typical_weight:
                if len(self.children) == 2:
                    raise NotImplementedError("Cannot handle two imbalanced children")
                return _WeightImbalance(child.name, 0, typical_weight)

    def weight_imbalance(
        self, expected_weight: Optional[int] = None
    ) -> Optional[_WeightImbalance]:
        weight_with_children = self.total_weight()
        if expected_weight is None:
            expected_weight = weight_with_children
        imbalanced_child = self._imbalanced_child()
        if imbalanced_child is not None:
            child = next(
                child for child in self.children if child.name == imbalanced_child.node
            )
            return child.weight_imbalance(imbalanced_child.expected_weight)
        if expected_weight != weight_with_children:
            return _WeightImbalance(
                self.name,
                self.weight,
                expected_weight - weight_with_children + self.weight,
            )
        return None


class TreeBuilder:
    def __init__(self) -> None:
        self._nodes = {}

    def add_node(self, name: str, weight: int, children: list[str] = None) -> None:
        if children is None:
            children = []
        new_node = self._nodes.get(name, TreeNode(name, weight, None, []))
        children_nodes = []
        for child in children:
            if child in self._nodes:
                self._nodes[child].parent = new_node
            else:
                self._nodes[child] = TreeNode(child, 0, new_node, [])
            children_nodes.append(self._nodes[child])
        new_node.children = children_nodes
        new_node.weight = weight
        if name not in self._nodes:
            self._nodes[name] = new_node

    def root(self) -> Optional[TreeNode]:
        if not self._nodes:
            return None
        node = next(iter(self._nodes.values()))
        while node.parent is not None:
            node = node.parent
        return node
