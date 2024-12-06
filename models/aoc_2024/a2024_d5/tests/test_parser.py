from models.common.io import InputFromString

from ..logic import PageOrderingRule
from ..parser import parse_page_ordering_rules, parse_updates

_CONTENT = """
           47|53
           97|13

           75,29,13
           75,97,47,61,53
           """


def test_parse_page_ordering_rules():
    input_reader = InputFromString(_CONTENT)
    rules = list(parse_page_ordering_rules(input_reader))
    assert rules == [
        PageOrderingRule(page_before=47, page_after=53),
        PageOrderingRule(page_before=97, page_after=13),
    ]


def test_parse_updates():
    input_reader = InputFromString(_CONTENT)
    updates = list(parse_updates(input_reader))
    assert updates == [
        (75, 29, 13),
        (75, 97, 47, 61, 53),
    ]
