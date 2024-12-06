from typing import Iterator

from models.common.io import InputReader

from .customs_group import CustomsGroup


def parse_form_answers_by_groups(input_reader: InputReader) -> Iterator[CustomsGroup]:
    current_group = CustomsGroup()
    for line in input_reader.read_stripped_lines(keep_empty_lines=True):
        if line:
            current_group.add_individual_answers(set(line))
        else:
            if current_group.answers:
                yield current_group
            current_group = CustomsGroup()
    if current_group.answers:
        yield current_group
