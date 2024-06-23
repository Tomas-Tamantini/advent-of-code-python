from models.common.io import IOHandler
from .parser import parse_guard_logs


def aoc_2018_d4(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2018, 4, "Repose Record")
    guards = list(parse_guard_logs(io_handler.input_reader))
    guard_most_asleep = max(guards, key=lambda g: g.total_minutes_asleep)
    minute_most_asleep = guard_most_asleep.minute_most_likely_to_be_asleep()
    product = guard_most_asleep.id * minute_most_asleep
    print(f"Part 1: Guard most asleep has product {product}")
    guard_most_asleep_on_same_minute = max(
        guards,
        key=lambda g: g.num_times_slept_on_minute(g.minute_most_likely_to_be_asleep()),
    )
    minute_most_asleep_on_same_minute = (
        guard_most_asleep_on_same_minute.minute_most_likely_to_be_asleep()
    )
    product = guard_most_asleep_on_same_minute.id * minute_most_asleep_on_same_minute
    print(f"Part 2: Guard most asleep on same minute has product {product}")
