from models.common.io import InputFromString
from ..parser import parse_scratchcards


def test_parse_scratchcards():
    file_content = """
                   Card 7: 41 48 83 | 83 86  6 31
                   Card 2: 13 32 20 61 | 61 30
                   """
    input_reader = InputFromString(file_content)

    cards = list(parse_scratchcards(input_reader))
    assert len(cards) == 2
    assert cards[0].card_id == 7
    assert cards[0].winning_numbers == {41, 48, 83}
    assert cards[0].chosen_numbers == {83, 86, 6, 31}
    assert cards[1].card_id == 2
    assert cards[1].winning_numbers == {13, 32, 20, 61}
    assert cards[1].chosen_numbers == {61, 30}
