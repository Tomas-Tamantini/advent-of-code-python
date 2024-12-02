def _report_is_safe(report: tuple[int, ...]) -> bool:
    if len(report) < 2:
        return True
    sign = report[1] - report[0]
    for i in range(1, len(report)):
        diff = report[i] - report[i - 1]
        if diff * sign <= 0 or abs(diff) > 3:
            return False
    return True


def report_is_safe(report: tuple[int, ...], num_bad_levels_tolerance: int = 0) -> bool:
    if _report_is_safe(report):
        return True
    elif num_bad_levels_tolerance == 0:
        return False
    else:
        for i in range(len(report)):
            new_report = report[:i] + report[i + 1 :]
            if report_is_safe(new_report, num_bad_levels_tolerance - 1):
                return True
    return False
