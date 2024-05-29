from .password_generator import PasswordGenerator


def test_indices_that_make_hash_start_with_n_zeroes_are_generated():
    password_generator = PasswordGenerator("abc", num_zeroes=3, password_length=5)
    indices_generator = password_generator.indices_whose_hash_start_with_zeroes()
    assert next(indices_generator)[0] == 2196
    assert next(indices_generator)[0] == 3527


def test_can_generate_password_from_left_to_right():
    password_generator = PasswordGenerator("abc", num_zeroes=3, password_length=5)
    password_generator.generate_passwords()
    assert password_generator.password_left_to_right == "d8d60"


def test_can_generate_password_one_position_at_a_time():
    password_generator = PasswordGenerator("dce", num_zeroes=3, password_length=5)
    password_generator.generate_passwords()
    assert password_generator.password_one_position_at_a_time == "943e2"
