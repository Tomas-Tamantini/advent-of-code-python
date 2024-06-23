from models.common.io import IOHandler
from .parser import parse_plane_seat_ids


def aoc_2020_d5(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2020, 5, "Binary Boarding")
    seat_ids = sorted(parse_plane_seat_ids(io_handler.input_reader))
    max_id = seat_ids[-1]
    print(f"Part 1: The highest seat ID is {max_id}")
    for i, seat_id in enumerate(seat_ids):
        if seat_ids[i + 1] - seat_id == 2:
            missing_seat_id = seat_id + 1
            break
    print(f"Part 2: The missing seat ID is {missing_seat_id}")
