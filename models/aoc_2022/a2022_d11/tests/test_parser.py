from models.common.io import InputFromString
from ..parser import parse_monkeys


def test_parse_monkeys():
    input_reader = InputFromString(
        """
        Monkey 1:
        Starting items: 54, 65, 75, 74
        Operation: new = old + 6
        Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0

        Monkey 2:
        Starting items: 79, 60, 97
        Operation: new = old * old
        Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3
        """
    )
    monkeys = list(parse_monkeys(input_reader, boredom_worry_level_divisor=3))
    assert len(monkeys) == 2
    assert monkeys[0].dequeue_item() == 20
    assert monkeys[1].dequeue_item() == 2080
    assert monkeys[0].next_monkey_index(38) == 2
    assert monkeys[0].next_monkey_index(39) == 0
    assert monkeys[1].next_monkey_index(52) == 1
    assert monkeys[1].next_monkey_index(12) == 3
