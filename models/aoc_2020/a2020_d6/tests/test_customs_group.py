from ..customs_group import CustomsGroup


def test_can_list_questions_to_which_at_least_one_person_answered_yes():
    group = CustomsGroup()
    group.add_individual_answers({"a", "b", "c"})
    group.add_individual_answers({"a", "c"})
    group.add_individual_answers({"a", "b", "d"})
    assert group.questions_with_at_least_one_yes() == {"a", "b", "c", "d"}


def test_can_list_questions_to_which_everyone_answered_yes():
    group = CustomsGroup()
    group.add_individual_answers({"a", "b", "c"})
    group.add_individual_answers({"a", "c"})
    group.add_individual_answers({"a", "b", "d"})
    assert group.questions_everyone_answered_yes() == {"a"}
