from typing import Iterator, Hashable


class DisjointSet:
    def __init__(self) -> None:
        self._parents = dict()
        self._ranks = dict()
        self._num_sets = 0

    @property
    def num_sets(self) -> int:
        return self._num_sets

    def make_set(self, element: Hashable) -> None:
        self._parents[element] = element
        self._ranks[element] = 0
        self._num_sets += 1

    def find(self, element: Hashable) -> Hashable:
        if self._parents[element] != element:
            self._parents[element] = self.find(self._parents[element])
        return self._parents[element]

    def union(self, element1: Hashable, element2: Hashable) -> None:
        root1 = self.find(element1)
        root2 = self.find(element2)
        if root1 != root2:
            self._num_sets -= 1
            if self._ranks[root1] > self._ranks[root2]:
                self._parents[root2] = root1
            else:
                self._parents[root1] = root2
                if self._ranks[root1] == self._ranks[root2]:
                    self._ranks[root2] += 1
