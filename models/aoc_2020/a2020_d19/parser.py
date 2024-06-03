from models.common.io import InputReader
from typing import Hashable
from models.common.assembly import ContextFreeGrammar


def parse_context_free_grammar_and_words(
    input_reader: InputReader, starting_symbol: Hashable
) -> tuple[ContextFreeGrammar, list[str]]:
    cfg = ContextFreeGrammar(starting_symbol)
    words = []
    lines = list(input_reader.read_stripped_lines())
    for line in lines:
        if ":" in line:
            parts = line.split(":")
            symbol = int(parts[0])
            for production in parts[1].split("|"):
                if '"' in production:
                    terminal = production.strip().replace('"', "")
                    cfg.add_rule(symbol, production=(terminal,))
                else:
                    cfg.add_rule(symbol, production=tuple(map(int, production.split())))
        else:
            words.append(line)
    return cfg, words
