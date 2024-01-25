from dataclasses import dataclass


@dataclass
class NavigationTreeNode:
    metadata: list[int]
    children: list["NavigationTreeNode"]

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def sum_of_metadata(self) -> int:
        return sum(self.metadata) + sum(
            child.sum_of_metadata() for child in self.children
        )


def parse_list_into_navigation_tree(numbers: list[int]) -> NavigationTreeNode:
    def parse_node(numbers: list[int]) -> tuple[NavigationTreeNode, list[int]]:
        n_children = numbers.pop(0)
        n_metadata = numbers.pop(0)
        children = []
        for _ in range(n_children):
            child, numbers = parse_node(numbers)
            children.append(child)
        metadata = numbers[:n_metadata]
        numbers = numbers[n_metadata:]
        return NavigationTreeNode(metadata=metadata, children=children), numbers

    root, _ = parse_node(numbers)
    return root
