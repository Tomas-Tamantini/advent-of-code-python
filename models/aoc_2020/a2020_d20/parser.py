from typing import Iterator

from models.common.io import InputReader

from .logic import JigsawPieceBinaryImage


def parse_jigsaw_pieces(input_reader: InputReader) -> Iterator[JigsawPieceBinaryImage]:
    lines = list(input_reader.readlines())
    current_id = -1
    current_rows = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if "Tile" in stripped_line:
            if current_id != -1:
                yield JigsawPieceBinaryImage.from_string(current_id, current_rows)
            current_id = int(stripped_line.split(" ")[1].replace(":", ""))
            current_rows = []
        else:
            current_rows.append(stripped_line)
    if current_id != -1:
        yield JigsawPieceBinaryImage.from_string(current_id, current_rows)
