from models.common.io import InputFromString

from .parser import parse_plane_seat_ids


def test_parse_plane_seat_ids():
    file_content = """
                   BFFFBBFRRR
                   FFFBBBFRRR
                   BBFFBBFRLL
                   """
    seat_ids = list(parse_plane_seat_ids(InputFromString(file_content)))
    assert seat_ids == [567, 119, 820]
