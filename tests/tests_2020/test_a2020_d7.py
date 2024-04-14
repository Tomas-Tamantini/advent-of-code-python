from models.aoc_2020 import LuggageRule, LuggageRules


def test_luggage_rules_restrict_color_of_outermost_bag():
    rules = LuggageRules()
    rules.add_rule(LuggageRule("light red", {"bright white": 1, "muted yellow": 2}))
    rules.add_rule(LuggageRule("dark orange", {"bright white": 3, "muted yellow": 4}))
    rules.add_rule(LuggageRule("bright white", {"shiny gold": 1}))
    rules.add_rule(LuggageRule("muted yellow", {"shiny gold": 2, "faded blue": 9}))
    rules.add_rule(LuggageRule("shiny gold", {"dark olive": 1, "vibrant plum": 2}))
    rules.add_rule(LuggageRule("dark olive", {"faded blue": 3, "dotted black": 4}))
    rules.add_rule(LuggageRule("vibrant plum", {"faded blue": 5, "dotted black": 6}))
    rules.add_rule(LuggageRule("faded blue", {}))
    rules.add_rule(LuggageRule("dotted black", {}))
    possible_colors = list(rules.possible_colors_of_outermost_bag("shiny gold"))
    assert len(possible_colors) == 4
    assert set(possible_colors) == {
        "bright white",
        "muted yellow",
        "dark orange",
        "light red",
    }
