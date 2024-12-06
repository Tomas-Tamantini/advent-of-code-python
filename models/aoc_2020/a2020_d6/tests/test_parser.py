from models.common.io import InputFromString

from ..parser import parse_form_answers_by_groups


def test_parse_form_answers_by_groups():
    file_content = """
                   abc

                   a
                   b
                   c

                   ab
                   ac

                   a
                   a
                   a
                   a

                   b
                   """
    groups = list(parse_form_answers_by_groups(InputFromString(file_content)))
    assert len(groups) == 5
    assert groups[0].answers == [{"a", "b", "c"}]
    assert groups[1].answers == [{"a"}, {"b"}, {"c"}]
    assert groups[2].answers == [{"a", "b"}, {"a", "c"}]
    assert groups[3].answers == [{"a"}, {"a"}, {"a"}, {"a"}]
    assert groups[4].answers == [{"b"}]
