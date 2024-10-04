from models.common.io import InputReader, CharacterGrid
from .logic import MirrorContraption, Mirror, Splitter


def parse_mirror_contraption(input_reader: InputReader) -> MirrorContraption:
    _symbols = {
        "\\": Mirror(is_upward_diagonal=False),
        "/": Mirror(is_upward_diagonal=True),
        "-": Splitter(is_horizontal=True),
        "|": Splitter(is_horizontal=False),
    }
    grid = CharacterGrid(text=input_reader.read())
    cells = dict()
    for symbol, cell in _symbols.items():
        for pos in grid.positions_with_value(symbol):
            cells[pos] = cell
    return MirrorContraption(grid.width, grid.height, cells)
