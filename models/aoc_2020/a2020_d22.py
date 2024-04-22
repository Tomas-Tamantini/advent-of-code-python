class CrabCombat:
    def __init__(self, cards_a: list[int], cards_b: list[int]) -> None:
        self._cards_a = cards_a
        self._cards_b = cards_b

    @property
    def cards_a(self) -> list[int]:
        return self._cards_a

    @property
    def cards_b(self) -> list[int]:
        return self._cards_b

    @property
    def winning_cards(self) -> list[int]:
        return self._cards_a or self._cards_b

    def winning_score(self) -> int:
        return sum(
            card * (i + 1) for i, card in enumerate(reversed(self.winning_cards))
        )

    def play_round(self) -> None:
        card_a = self._cards_a.pop(0)
        card_b = self._cards_b.pop(0)
        if card_a > card_b:
            self._cards_a.extend([card_a, card_b])
        else:
            self._cards_b.extend([card_b, card_a])

    def play_game(self) -> None:
        while self._cards_a and self._cards_b:
            self.play_round()
