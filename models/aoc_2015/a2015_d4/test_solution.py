from .solution import md5_hash, mine_advent_coins


def test_md5_hash_returns_hashed_value_in_hexadecimal_form():
    assert md5_hash("abcdef609043") == "000001dbbfa3a5c83a2d506429c7b00e"
    assert md5_hash("pqrstuv1048970") == "000006136ef2ff3b291c85725f17325c"


def test_value_which_makes_hash_start_with_n_zeros_is_found():
    assert mine_advent_coins("abcdef", num_leading_zeros=5) == 609043
