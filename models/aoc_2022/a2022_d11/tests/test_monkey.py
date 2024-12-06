from typing import Callable

from ..monkey import Monkey, Monkeys, NextMonkeyIndexRule


def _build_monkey(
    worry_level_transformation: Callable[[int], int] = None,
    boredom_worry_level_divisor: int = 3,
    next_monkey_index_rule: NextMonkeyIndexRule = None,
):
    if worry_level_transformation is None:
        worry_level_transformation = lambda w: w
    if next_monkey_index_rule is None:
        next_monkey_index_rule = NextMonkeyIndexRule(
            divisor=2, index_if_divisible=1, index_if_not_divisible=0
        )
    return Monkey(
        worry_level_transformation, boredom_worry_level_divisor, next_monkey_index_rule
    )


def test_monkey_starts_with_no_items():
    monkey = _build_monkey()
    assert monkey.empty_handed
    assert monkey.num_items_inspected == 0


def test_giving_item_to_monkey_makes_it_not_empty_handed():
    monkey = _build_monkey()
    monkey.give_item(worry_level=100)
    assert not monkey.empty_handed
    assert monkey.num_items_inspected == 0


def test_monkey_inspects_and_transforms_items_worry_level_before_removing_it_from_queue():
    monkey = _build_monkey(
        worry_level_transformation=lambda w: 2 * w,
        boredom_worry_level_divisor=3,
    )
    monkey.give_item(123)
    monkey.give_item(456)
    popped_worry_level = monkey.dequeue_item()
    assert popped_worry_level == 82  # 2 * 123 // 3
    assert monkey.num_items_inspected == 1
    popped_worry_level = monkey.dequeue_item()
    assert popped_worry_level == 304  # 2 * 456 // 3
    assert monkey.num_items_inspected == 2


def test_monkey_decides_index_of_monkey_to_give_item_to_based_on_its_worry_level():
    monkey = _build_monkey(
        next_monkey_index_rule=NextMonkeyIndexRule(
            divisor=2, index_if_divisible=7, index_if_not_divisible=13
        ),
    )
    assert monkey.next_monkey_index(worry_level=7) == 13
    assert monkey.next_monkey_index(worry_level=8) == 7


def _example_monkeys(boredom_worry_level_divisor: int = 3) -> tuple[Monkey]:
    monkeys = (
        Monkey(
            worry_level_transformation=lambda w: 19 * w,
            boredom_worry_level_divisor=boredom_worry_level_divisor,
            next_monkey_index_rule=NextMonkeyIndexRule(
                divisor=23, index_if_divisible=2, index_if_not_divisible=3
            ),
        ),
        Monkey(
            worry_level_transformation=lambda w: 6 + w,
            boredom_worry_level_divisor=boredom_worry_level_divisor,
            next_monkey_index_rule=NextMonkeyIndexRule(
                divisor=19, index_if_divisible=2, index_if_not_divisible=0
            ),
        ),
        Monkey(
            worry_level_transformation=lambda w: w * w,
            boredom_worry_level_divisor=boredom_worry_level_divisor,
            next_monkey_index_rule=NextMonkeyIndexRule(
                divisor=13, index_if_divisible=1, index_if_not_divisible=3
            ),
        ),
        Monkey(
            worry_level_transformation=lambda w: 3 + w,
            boredom_worry_level_divisor=boredom_worry_level_divisor,
            next_monkey_index_rule=NextMonkeyIndexRule(
                divisor=17, index_if_divisible=0, index_if_not_divisible=1
            ),
        ),
    )

    starting_items = {
        0: (79, 98),
        1: (54, 65, 75, 74),
        2: (79, 60, 97),
        3: (74,),
    }
    for i, worry_levels in starting_items.items():
        for worry_level in worry_levels:
            monkeys[i].give_item(worry_level)

    return monkeys


def test_monkeys_throw_items_to_each_other_in_turn_during_round():
    monkeys = _example_monkeys()
    keep_away_monkeys = Monkeys(monkeys)
    keep_away_monkeys.play_round()

    assert monkeys[0].empty_handed == monkeys[1].empty_handed == False
    assert monkeys[2].empty_handed == monkeys[3].empty_handed == True

    expected_num_inspections = (2, 4, 3, 5)
    assert expected_num_inspections == tuple(keep_away_monkeys.num_inspections())


def test_monkeys_can_play_multiple_keep_away_rounds_efficiently():
    monkeys = _example_monkeys(boredom_worry_level_divisor=1)
    keep_away_monkeys = Monkeys(monkeys)
    for _ in range(1000):
        keep_away_monkeys.play_round()

    expected_num_inspections = (5204, 4792, 199, 5192)
    assert expected_num_inspections == tuple(keep_away_monkeys.num_inspections())
