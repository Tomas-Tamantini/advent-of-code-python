from models.common.io import InputFromString

from .parser import parse_context_free_grammar_and_words


def test_parse_context_free_grammar_and_words():
    file_content = """
                   0: 4 1 5
                   1: 2 3 | 3 2
                   2: 4 4 | 5 5
                   3: 4 5 | 5 4
                   4: "a"
                   5: "b"
 
                   ababbb
                   bababa
                   abbbab
                   aaabbb
                   aaaabbb
                   """
    cfg, words = parse_context_free_grammar_and_words(
        InputFromString(file_content), starting_symbol=0
    )
    assert words == ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"]
    assert cfg.matches(tuple("ababbb"))
    assert not cfg.matches(tuple("aaabbb"))
