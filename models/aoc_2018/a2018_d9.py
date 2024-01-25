from dataclasses import dataclass


@dataclass
class _Node:
    value: int
    prev: "_Node"
    next: "_Node"


class CircularLinkedList:
    def __init__(self) -> None:
        self._num_elements = 0
        self._element_at_head = None

    def add_at_head(self, element: int) -> None:
        if self._num_elements == 0:
            self._element_at_head = _Node(element, None, None)
            self._element_at_head.prev = self._element_at_head
            self._element_at_head.next = self._element_at_head
        else:
            new_node = _Node(element, self._element_at_head.prev, self._element_at_head)
            self._element_at_head.prev.next = new_node
            self._element_at_head.prev = new_node
            self._element_at_head = new_node

        self._num_elements += 1

    def pop_at_head(self) -> int:
        if self._num_elements == 0:
            raise IndexError("Cannot pop from empty list")
        value = self._element_at_head.value
        if self._num_elements == 1:
            self._element_at_head = None
        else:
            self._element_at_head.prev.next = self._element_at_head.next
            self._element_at_head.next.prev = self._element_at_head.prev
            self._element_at_head = self._element_at_head.next
        self._num_elements -= 1
        return value

    def rotate(self, steps: int) -> None:
        if self._num_elements == 0:
            return
        if steps >= 0:
            for _ in range(steps):
                self._element_at_head = self._element_at_head.next
        else:
            for _ in range(abs(steps)):
                self._element_at_head = self._element_at_head.prev

    def __len__(self):
        return self._num_elements

    @property
    def value_at_head(self) -> int:
        if self._num_elements == 0:
            raise IndexError("Cannot get element from empty list")
        return self._element_at_head.value


def marble_game_score(num_players: int, last_marble: int) -> dict[int, int]:
    scores = {i: 0 for i in range(1, num_players + 1)}
    cll = CircularLinkedList()
    cll.add_at_head(0)
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            cll.rotate(steps=-7)
            player_idx = (marble - 1) % num_players + 1
            scores[player_idx] += marble + cll.pop_at_head()
        else:
            cll.rotate(steps=2)
            cll.add_at_head(marble)
    return scores
