from typing import Hashable


class CrabCombat:
    def __init__(
        self,
        cards_a: list[int],
        cards_b: list[int],
        play_recursive: bool,
    ) -> None:
        self._cards_a = cards_a[:]
        self._cards_b = cards_b[:]
        self._play_recursive = play_recursive
        self._visited_states = set()

    @property
    def cards_a(self) -> list[int]:
        return self._cards_a

    @property
    def cards_b(self) -> list[int]:
        return self._cards_b

    @property
    def winning_cards(self) -> list[int]:
        return self._cards_a or self._cards_b

    def _winner_idx(self) -> int:
        return 0 if self._cards_a else 1

    def winning_score(self) -> int:
        return sum(
            card * (i + 1) for i, card in enumerate(reversed(self.winning_cards))
        )

    def _state(self) -> Hashable:
        return (tuple(self._cards_a), tuple(self._cards_b))

    def _round_winner(self) -> int:
        card_a = self._cards_a[0]
        card_b = self._cards_b[0]
        if (
            not self._play_recursive
            or len(self._cards_a) <= card_a
            or len(self._cards_b) <= card_b
        ):
            return 0 if card_a > card_b else 1
        else:
            subgame = CrabCombat(
                cards_a=self._cards_a[1 : card_a + 1],
                cards_b=self._cards_b[1 : card_b + 1],
                play_recursive=True,
            )
            subgame.play_game()
            return subgame._winner_idx()

    def play_round(self) -> None:
        winner = self._round_winner()
        card_a = self._cards_a.pop(0)
        card_b = self._cards_b.pop(0)
        if winner == 0:
            self._cards_a.extend([card_a, card_b])
        else:
            self._cards_b.extend([card_b, card_a])

    def play_game(self) -> None:
        while self._cards_a and self._cards_b:
            if self._state() in self._visited_states:
                self._cards_b.clear()
            else:
                self._visited_states.add(self._state())
                self.play_round()
