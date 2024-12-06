from collections import defaultdict
from itertools import combinations
from queue import Queue
from typing import Iterator

from .brick import Brick


class BricksDag:
    def __init__(self, bricks: set[Brick]) -> None:
        self._bricks = bricks
        self._supported_by = defaultdict(set)
        self._supports = defaultdict(set)
        self._calculate_connections()

    def _calculate_connections(self) -> None:
        for brick_a, brick_b in combinations(self._bricks, 2):
            if brick_a.sits_on_top(brick_b):
                self._supported_by[brick_a].add(brick_b)
                self._supports[brick_b].add(brick_a)
            elif brick_b.sits_on_top(brick_a):
                self._supported_by[brick_b].add(brick_a)
                self._supports[brick_a].add(brick_b)

    def _brick_must_topple(self, brick: Brick, toppled_bricks: set[Brick]) -> bool:
        return self._supported_by[brick].issubset(toppled_bricks)

    def bricks_that_would_topple(self, brick_to_remove: Brick) -> Iterator[Brick]:
        toppled = {brick_to_remove}
        check_topple_queue = Queue()

        for next_brick in self._supports[brick_to_remove]:
            check_topple_queue.put(next_brick)

        while not check_topple_queue.empty():
            brick = check_topple_queue.get()
            if self._brick_must_topple(brick, toppled):
                yield brick
                toppled.add(brick)
                for next_brick in self._supports[brick]:
                    if next_brick not in toppled:
                        check_topple_queue.put(next_brick)
