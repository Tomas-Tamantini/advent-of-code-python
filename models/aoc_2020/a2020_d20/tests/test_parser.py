from models.common.io import InputFromString

from ..parser import parse_jigsaw_pieces


def test_parse_jigsaw_pieces():
    file_content = """
                   Tile 2311:
                   .#.
                   ...

                   Tile 1951:
                   ..#
                   ###
                   """
    pieces = list(parse_jigsaw_pieces(InputFromString(file_content)))
    assert pieces[0].piece_id == 2311
    assert pieces[0].render() == ".#.\n..."
    assert pieces[1].piece_id == 1951
    assert pieces[1].render() == "..#\n###"
