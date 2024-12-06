from models.common.io import InputReader


def parse_crab_combat_cards(input_reader: InputReader) -> tuple[list[int], list[int]]:
    cards_a = []
    cards_b = []
    reading_player_b = False
    for line in input_reader.read_stripped_lines():
        if "Player 1" in line:
            reading_player_b = False
        elif "Player 2" in line:
            reading_player_b = True
        elif reading_player_b:
            cards_b.append(int(line))
        else:
            cards_a.append(int(line))
    return cards_a, cards_b
