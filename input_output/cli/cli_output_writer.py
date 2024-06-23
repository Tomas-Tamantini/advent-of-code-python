class CliOutputWriter:
    def write_header(self, year: int, day: int, problem_title: str) -> None:
        print(f"--- AOC {year} - Day {day}: {problem_title} ---")
