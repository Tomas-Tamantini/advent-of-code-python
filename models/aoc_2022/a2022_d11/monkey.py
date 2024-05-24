from typing import Callable
from queue import Queue


class Monkey:
    def __init__(
        self,
        worry_level_transformation: Callable[[int], int],
        boredom_worry_level_divisor: int,
        next_monkey_index_rule: Callable[[int], int],
    ) -> None:
        self._items_queue = Queue()
        self._num_items_inspected = 0
        self._worry_level_transformation = worry_level_transformation
        self._boredom_worry_level_divisor = boredom_worry_level_divisor
        self._next_monkey_index_rule = next_monkey_index_rule

    def give_item(self, worry_level: int) -> None:
        self._items_queue.put(worry_level)

    @property
    def empty_handed(self) -> bool:
        return self._items_queue.empty()

    @property
    def num_items_inspected(self) -> int:
        return self._num_items_inspected

    def dequeue_item(self) -> int:
        worry_level = self._items_queue.get()
        self._num_items_inspected += 1
        return (
            self._worry_level_transformation(worry_level)
            // self._boredom_worry_level_divisor
        )

    def next_monkey_index(self, worry_level: int) -> int:
        return self._next_monkey_index_rule(worry_level)


class Monkeys:
    def __init__(self, monkeys: tuple[Monkey]) -> None:
        self._monkeys = monkeys

    def play_round(self) -> None:
        for monkey in self._monkeys:
            while not monkey.empty_handed:
                worry_level = monkey.dequeue_item()
                next_monkey_index = monkey.next_monkey_index(worry_level)
                self._monkeys[next_monkey_index].give_item(worry_level)

    def num_inspections(self) -> list[int]:
        return [monkey.num_items_inspected for monkey in self._monkeys]
