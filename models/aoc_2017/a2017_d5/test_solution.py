from .solution import follow_and_increment_jump_instructions


def test_jump_instructions_are_followed_and_incremented_until_they_lead_outside_the_list():
    jump_instructions = [0, 3, 0, 1, -3]
    result = list(
        follow_and_increment_jump_instructions(
            jump_instructions, increment_rule=lambda jump: jump + 1
        )
    )
    expected_positions = [0, 0, 1, 4, 1]
    assert result == expected_positions


def test_can_follow_different_rules_to_increment_jump_instructions():
    jump_instructions = [0, 3, 0, 1, -3]
    result = list(
        follow_and_increment_jump_instructions(
            jump_instructions,
            increment_rule=lambda jump: jump - 1 if jump >= 3 else jump + 1,
        )
    )
    assert len(result) == 10
