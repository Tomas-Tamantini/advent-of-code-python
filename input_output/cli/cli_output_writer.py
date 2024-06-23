from typing import Optional


class CliOutputWriter:
    def write_header(self, year: int, day: int, problem_title: str) -> None:
        print(f"--- AOC {year} - Day {day}: {problem_title} ---")

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None:
        msg = f"Be patient, it takes about {time_estimation} to run"
        if part is not None:
            msg = f"Part {part}: {msg}"
        print(msg, end="\r")
