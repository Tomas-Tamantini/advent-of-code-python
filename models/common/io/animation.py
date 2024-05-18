from time import sleep


def render_frame(frame: str, sleep_seconds: float) -> None:
    num_lines = frame.count("\n")
    print(frame)
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    sleep(sleep_seconds)
    for _ in range(num_lines + 1):
        print(LINE_UP, end=LINE_CLEAR)
