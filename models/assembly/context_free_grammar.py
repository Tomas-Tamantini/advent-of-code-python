from typing import Hashable
from collections import defaultdict


class ContextFreeGrammar:
    def __init__(self, starting_symbol: Hashable) -> None:
        self._starting_symbol = starting_symbol
        self._rules = defaultdict(list)

    def add_rule(self, symbol: Hashable, production: tuple[Hashable, ...]) -> None:
        self._rules[symbol].append(production)

    def matches(self, word: tuple[Hashable, ...]) -> bool:
        return self._matches_recursive(
            word=word,
            symbols=(self._starting_symbol,),
            word_pointer=0,
            symbol_pointer=0,
        )

    def _matches_recursive(
        self,
        word: tuple[Hashable, ...],
        symbols: tuple[Hashable, ...],
        word_pointer: int,
        symbol_pointer: int,
    ) -> bool:
        if word_pointer == len(word) and symbol_pointer == len(symbols):
            return True
        if word_pointer == len(word) or symbol_pointer == len(symbols):
            return False
        symbol = symbols[symbol_pointer]
        if symbol in self._rules:
            for production in self._rules[symbol]:
                if self._matches_recursive(
                    word=word,
                    symbols=symbols[:symbol_pointer]
                    + production
                    + symbols[symbol_pointer + 1 :],
                    word_pointer=word_pointer,
                    symbol_pointer=symbol_pointer,
                ):
                    return True

        if word[word_pointer] == symbol:
            return self._matches_recursive(
                word=word,
                symbols=symbols,
                word_pointer=word_pointer + 1,
                symbol_pointer=symbol_pointer + 1,
            )
        return False
