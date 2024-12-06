from models.common.io import InputReader

from .programmable_screen import ProgrammableScreen


def parse_programmable_screen_instructions(
    input_reader: InputReader, screen: ProgrammableScreen
) -> None:
    for line in input_reader.readlines():
        if "rect" in line:
            width, height = map(int, line.split("rect")[-1].strip().split("x"))
            screen.rect(width, height)
        elif "rotate row" in line:
            row, offset = map(
                int, line.replace("y=", "").split("row")[-1].strip().split(" by ")
            )
            screen.rotate_row(row, offset)
        elif "rotate column" in line:
            column, offset = map(
                int,
                line.replace("x=", "").split("column")[-1].strip().split(" by "),
            )
            screen.rotate_column(column, offset)
