from collections import defaultdict
from datetime import datetime
from typing import Iterator

from models.common.io import InputReader

from .napping_guard import Guard, GuardNap


def parse_guard_logs(input_reader: InputReader) -> Iterator[Guard]:
    lines = [l.strip() for l in input_reader.readlines()]
    sorted_lines = sorted(lines, key=lambda l: l[:18])
    guard_logs = defaultdict(list)
    guard_id = -1
    for line in sorted_lines:
        if not line:
            continue
        if "Guard" in line:
            guard_id = int(line.split()[-3].replace("#", ""))
        else:
            event_time = datetime.strptime(line.split("]")[0] + "]", "[%Y-%m-%d %H:%M]")
            guard_logs[guard_id].append(event_time)
    for guard_id, nap_records in guard_logs.items():
        naps = []
        for i in range(0, len(nap_records), 2):
            start = nap_records[i]
            end = nap_records[i + 1]
            naps.append(GuardNap(start, end))
        yield Guard(guard_id, naps)
