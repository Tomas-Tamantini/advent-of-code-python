import pytest
from .key_generator import KeyGenerator


def test_key_are_generated_properly():
    key_generator = KeyGenerator(
        salt="abc",
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
    )
    indices = key_generator.indices_which_produce_keys(num_indices=64)
    assert len(indices) == 64
    assert indices[:2] == [39, 92]
    assert indices[-1] == 22728


@pytest.mark.skip(reason="Takes a couple of seconds")
def test_keys_can_be_generated_with_recursive_hashes():
    key_generator = KeyGenerator(
        salt="abc",
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
        num_hashes=2017,
    )
    indices = key_generator.indices_which_produce_keys(num_indices=1)
    assert len(indices) == 1
    assert indices[0] == 10
