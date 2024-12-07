import argparse
from input_output import run_solutions
from models.common.io import ExecutionFlags


def _parse_year_range(year_range: str) -> tuple[int, int]:
    if not year_range:
        return (2015, 2024)  # TODO: Get dynamically
    years = year_range.split("-")
    if len(years) == 1:
        return int(years[0]), int(years[0])
    first_year, last_year = int(years[0]), int(years[1])
    return min(first_year, last_year), max(first_year, last_year)


def _parse_day_range(day_range: str) -> tuple[int, int]:
    if not day_range:
        return (-1, -1)
    days = day_range.split("-")
    if len(days) == 1:
        return int(days[0]), int(days[0])
    first_day, last_day = int(days[0]), int(days[1])
    return min(first_day, last_day), max(first_day, last_day)


def _days_for_year(parsed_day_range: tuple[int, int], year: int) -> tuple[int, ...]:
    if not parsed_day_range or parsed_day_range[0] == -1:
        return tuple()  # TODO: Get days available for year dynamically
    else:
        return tuple(d for d in range(parsed_day_range[0], parsed_day_range[1] + 1))


def main(solutions_to_run, flags: ExecutionFlags) -> None:
    run_solutions(solutions_to_run, flags)


def _parse_solutions_to_run(args: argparse.Namespace) -> dict[int, tuple[int, ...]]:
    year_range = args.year
    if not year_range:
        year_range = (2015, 2024)  # TODO: Get dynamically
    days_range = args.day
    solutions_to_run = {
        y: _days_for_year(days_range, y)
        for y in range(year_range[0], year_range[1] + 1)
    }

    return solutions_to_run


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Advent of Code solutions")
    parser.add_argument(
        "-y",
        "--year",
        nargs="?",
        help="Run solutions for a specific year (ex. 2024) or range of years (ex. 2015-2024). If empty, all years will be run.",
        type=_parse_year_range,
    )
    parser.add_argument(
        "-d",
        "--day",
        nargs="?",
        help="Run solutions for a specific day (ex. 1) or range of days (ex. 1-25). If empty, all days will be run.",
        type=_parse_day_range,
    )
    parser.add_argument(
        "-a",
        "--animate",
        action="store_true",
        help="Display solution animations (if available)",
    )
    parser.add_argument(
        "-p",
        "--play",
        action="store_true",
        help="Play with interactive solutions (if available)",
    )
    parser.add_argument(
        "-c",
        "--check-results",
        action="store_true",
        help="Check results against expected results and generate a report",
    )

    args = parser.parse_args()
    solutions_to_run = _parse_solutions_to_run(args)
    flags = ExecutionFlags(
        animate=args.animate,
        play=args.play,
        check_results=args.check_results,
    )
    main(solutions_to_run, flags)
