from models.common.io import InputReader

from .luggage_rules import LuggageRule, LuggageRules


def _parse_luggage_rule(rule: str) -> LuggageRule:
    parts = rule.split("contain")
    container_bag = parts[0].strip().replace("bags", "").replace("bag", "").strip()

    contained_bags = dict()
    for part in parts[1].split(","):
        new_part = (
            part.strip().replace("bags", "").replace("bag", "").replace(".", "").strip()
        )
        if "no other" in new_part:
            continue
        quantity, bag = new_part.split(" ", 1)
        contained_bags[bag] = int(quantity)

    return LuggageRule(bag=container_bag, contains=contained_bags)


def parse_luggage_rules(input_reader: InputReader) -> LuggageRules:
    rules = LuggageRules()
    for line in input_reader.read_stripped_lines():
        rules.add_rule(_parse_luggage_rule(line))
    return rules
