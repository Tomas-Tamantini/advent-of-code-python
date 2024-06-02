from datetime import datetime
from models.common.io import InputFromString
from ..parser import parse_guard_logs
from ..napping_guard import GuardNap


def test_parse_shuffled_guard_logs():
    file_content = """[1518-11-04 00:02] Guard #99 begins shift
                      [1518-11-01 00:05] falls asleep
                      [1518-11-01 00:25] wakes up
                      [1518-11-01 00:30] falls asleep
                      [1518-11-01 00:55] wakes up
                      [1518-11-01 23:58] Guard #99 begins shift
                      [1518-11-05 00:03] Guard #99 begins shift
                      [1518-11-02 00:40] falls asleep
                      [1518-11-01 00:00] Guard #10 begins shift
                      [1518-11-02 00:50] wakes up
                      [1518-11-05 00:45] falls asleep
                      [1518-11-03 00:05] Guard #10 begins shift
                      [1518-11-03 00:24] falls asleep
                      [1518-11-03 00:29] wakes up
                      [1518-11-04 00:36] falls asleep
                      [1518-11-04 00:46] wakes up
                      [1518-11-05 00:55] wakes up"""
    guards = list(parse_guard_logs(InputFromString(file_content)))
    assert len(guards) == 2
    assert guards[0].id == 10
    assert guards[0].naps == [
        GuardNap(
            start_inclusive=datetime(1518, 11, 1, 0, 5),
            end_exclusive=datetime(1518, 11, 1, 0, 25),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 1, 0, 30),
            end_exclusive=datetime(1518, 11, 1, 0, 55),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 3, 0, 24),
            end_exclusive=datetime(1518, 11, 3, 0, 29),
        ),
    ]
    assert guards[1].id == 99
    assert guards[1].naps == [
        GuardNap(
            start_inclusive=datetime(1518, 11, 2, 0, 40),
            end_exclusive=datetime(1518, 11, 2, 0, 50),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 4, 0, 36),
            end_exclusive=datetime(1518, 11, 4, 0, 46),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 5, 0, 45),
            end_exclusive=datetime(1518, 11, 5, 0, 55),
        ),
    ]
