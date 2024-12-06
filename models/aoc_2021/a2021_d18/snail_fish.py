from dataclasses import dataclass
from typing import Optional, Protocol, Union


class SnailfishNodeProtocol(Protocol):
    def magnitude(self) -> int: ...

    def to_list(self) -> Union[int, list]: ...

    def try_explode(self, depth: int) -> bool: ...

    def try_split(self) -> bool: ...

    def add_to_leftmost_leaf(self, value: int) -> None: ...

    def add_to_rightmost_leaf(self, value: int) -> None: ...


@dataclass
class SnailfishNode:
    left_child: SnailfishNodeProtocol
    right_child: SnailfishNodeProtocol
    parent: Optional["SnailfishNode"] = None
    is_left_child: Optional[bool] = None

    def magnitude(self) -> int:
        return 3 * self.left_child.magnitude() + 2 * self.right_child.magnitude()

    def to_list(self) -> Union[int, list]:
        return [self.left_child.to_list(), self.right_child.to_list()]

    def try_split(self) -> bool:
        return self.left_child.try_split() or self.right_child.try_split()

    def try_explode(self, depth: int) -> bool:
        if depth < 4:
            return self.left_child.try_explode(
                depth + 1
            ) or self.right_child.try_explode(depth + 1)
        else:
            left_value = self.left_child.magnitude()
            right_value = self.right_child.magnitude()
            self.parent._add_to_next_leaf_to_the_left(
                left_value, came_from_left_child=self.is_left_child
            )
            self.parent._add_to_next_leaf_to_the_right(
                right_value, came_form_left_child=self.is_left_child
            )
            new_node = SnailfishLeaf(
                value=0, parent=self.parent, is_left_child=self.is_left_child
            )
            if self.is_left_child:
                self.parent.left_child = new_node
            else:
                self.parent.right_child = new_node
            return True

    def _add_to_next_leaf_to_the_left(
        self, value: int, came_from_left_child: bool
    ) -> None:
        if not came_from_left_child:
            self.left_child.add_to_rightmost_leaf(value)
        elif self.parent:
            self.parent._add_to_next_leaf_to_the_left(
                value, came_from_left_child=self.is_left_child
            )

    def _add_to_next_leaf_to_the_right(
        self, value: int, came_form_left_child: bool
    ) -> None:
        if came_form_left_child:
            self.right_child.add_to_leftmost_leaf(value)
        elif self.parent:
            self.parent._add_to_next_leaf_to_the_right(
                value, came_form_left_child=self.is_left_child
            )

    def add_to_leftmost_leaf(self, value: int) -> None:
        self.left_child.add_to_leftmost_leaf(value)

    def add_to_rightmost_leaf(self, value: int) -> None:
        self.right_child.add_to_rightmost_leaf(value)


@dataclass
class SnailfishLeaf:
    value: int
    parent: Optional[SnailfishNode] = None
    is_left_child: Optional[bool] = None

    def magnitude(self) -> int:
        return self.value

    def to_list(self) -> Union[int, list]:
        return self.value

    def try_explode(self, depth: int) -> bool:
        return False

    def try_split(self) -> bool:
        if self.value < 10:
            return False
        left_value = self.value // 2
        right_value = self.value - left_value
        new_node = SnailfishNode(
            left_child=SnailfishLeaf(value=left_value, is_left_child=True),
            right_child=SnailfishLeaf(value=right_value, is_left_child=False),
            parent=self.parent,
            is_left_child=self.is_left_child,
        )
        new_node.left_child.parent = new_node
        new_node.right_child.parent = new_node
        if self.is_left_child:
            self.parent.left_child = new_node
        else:
            self.parent.right_child = new_node
        return True

    def add_to_leftmost_leaf(self, value: int) -> None:
        self.value += value

    def add_to_rightmost_leaf(self, value: int) -> None:
        self.value += value


class SnailFishTree:
    def __init__(self, root: SnailfishNodeProtocol):
        self._root = root

    def magnitude(self) -> int:
        return self._root.magnitude()

    @classmethod
    def from_list(cls, fish_as_list: Union[int, list]) -> "SnailFishTree":
        root = SnailFishTree._fish_from_list(fish_as_list)
        return cls(root=root)

    @staticmethod
    def _fish_from_list(fish_as_list: Union[int, list]) -> SnailfishNodeProtocol:
        if isinstance(fish_as_list, int):
            return SnailfishLeaf(value=fish_as_list)
        else:
            node = SnailfishNode(
                left_child=SnailFishTree._fish_from_list(fish_as_list[0]),
                right_child=SnailFishTree._fish_from_list(fish_as_list[1]),
            )
            node.left_child.parent = node
            node.left_child.is_left_child = True
            node.right_child.parent = node
            node.right_child.is_left_child = False
            return node

    def to_list(self) -> Union[int, list]:
        return self._root.to_list()

    def reduce(self) -> None:
        change_happened = True
        while change_happened:
            change_happened = self._root.try_explode(depth=0) or self._root.try_split()

    def __add__(self, other: "SnailFishTree") -> "SnailFishTree":
        new_root = SnailfishNode(left_child=self._root, right_child=other._root)
        new_root.left_child.parent = new_root
        new_root.left_child.is_left_child = True
        new_root.right_child.parent = new_root
        new_root.right_child.is_left_child = False
        new_tree = SnailFishTree(root=new_root)
        new_tree.reduce()
        return new_tree
