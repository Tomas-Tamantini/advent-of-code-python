import pytest

from ..logic import PageOrderingRule, PageOrderingRules


def test_page_ordering_ignores_rules_not_involving_pages_in_update():
    rules = PageOrderingRules([PageOrderingRule(1, 2), PageOrderingRule(2, 3)])
    assert rules.is_in_correct_order((1, 3))
    assert rules.is_in_correct_order((3, 1))


_RULES = PageOrderingRules(
    [
        PageOrderingRule(47, 53),
        PageOrderingRule(97, 13),
        PageOrderingRule(97, 61),
        PageOrderingRule(97, 47),
        PageOrderingRule(75, 29),
        PageOrderingRule(61, 13),
        PageOrderingRule(75, 53),
        PageOrderingRule(29, 13),
        PageOrderingRule(97, 29),
        PageOrderingRule(53, 29),
        PageOrderingRule(61, 53),
        PageOrderingRule(97, 53),
        PageOrderingRule(61, 29),
        PageOrderingRule(47, 13),
        PageOrderingRule(75, 47),
        PageOrderingRule(97, 75),
        PageOrderingRule(47, 61),
        PageOrderingRule(75, 61),
        PageOrderingRule(47, 29),
        PageOrderingRule(75, 13),
        PageOrderingRule(53, 13),
    ]
)


@pytest.mark.parametrize(
    "update", [(75, 47, 61, 53, 29), (97, 61, 53, 29, 13), (75, 29, 13)]
)
def test_update_is_correctly_ordered_if_it_does_not_violate_any_rules(update):
    assert _RULES.is_in_correct_order(update)


@pytest.mark.parametrize(
    "update", [(75, 97, 47, 61, 53), (61, 13, 29), (97, 13, 75, 29, 47)]
)
def test_update_is_not_correctly_ordered_if_it_violates_any_rules(update):
    assert not _RULES.is_in_correct_order(update)


@pytest.mark.parametrize(
    ("update", "sorted_update"),
    [
        ((75, 97, 47, 61, 53), (97, 75, 47, 61, 53)),
        ((61, 13, 29), (61, 29, 13)),
        ((97, 13, 75, 29, 47), (97, 75, 47, 29, 13)),
    ],
)
def test_update_is_properly_sorted_according_to_page_ordering_rules(
    update, sorted_update
):
    assert sorted_update == _RULES.sort_update(update)
