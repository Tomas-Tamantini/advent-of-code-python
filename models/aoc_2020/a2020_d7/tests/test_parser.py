from models.common.io import InputFromString
from ..parser import parse_luggage_rules


def test_parse_luggage_rules():
    file_content = """
                   light red bags contain 1 bright white bag, 2 muted yellow bags.
                   dark orange bags contain 3 bright white bags, 4 muted yellow bags.
                   bright white bags contain 1 shiny gold bag.
                   muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
                   shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
                   dark olive bags contain 3 faded blue bags, 4 dotted black bags.
                   vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
                   faded blue bags contain no other bags.
                   dotted black bags contain no other bags.
                   """
    rules = parse_luggage_rules(InputFromString(file_content))
    assert set(rules.possible_colors_of_outermost_bag("shiny gold")) == {
        "bright white",
        "muted yellow",
        "dark orange",
        "light red",
    }
