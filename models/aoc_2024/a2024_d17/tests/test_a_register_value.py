from ..logic import a_register_value_to_produce_quine


def test_smallest_a_register_value_to_produce_quine_is_found():
    instructions = (0, 3, 5, 4, 3, 0)
    assert 117440 == a_register_value_to_produce_quine(instructions)
