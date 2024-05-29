from models.common.io import InputReader


def parse_code_row_and_col(input_reader: InputReader) -> dict[str, int]:
    text = input_reader.read()
    parts = text.replace(",", "").replace(".", "").split(" ")
    return {"row": int(parts[-3]), "col": int(parts[-1])}
