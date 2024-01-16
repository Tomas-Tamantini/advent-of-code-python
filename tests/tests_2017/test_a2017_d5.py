from models.aoc_2017 import follow_and_increment_jump_instructions


def test_jump_instructions_are_followed_and_incremented_until_they_lead_outside_the_list():
    jump_instructions = [0, 3, 0, 1, -3]
    expected_positions = [0, 0, 1, 4, 1]
    assert (
        list(follow_and_increment_jump_instructions(jump_instructions))
        == expected_positions
    )
