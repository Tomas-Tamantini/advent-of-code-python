from models.common.io import InputFromString
from ..parser import parse_program_tree


def test_parse_program_tree():
    file_content = """pbga (66)
                      xhth (57)
                      ebii (61)
                      havc (66)
                      ktlj (57)
                      fwft (72) -> ktlj, cntj, xhth
                      qoyq (66)
                      padx (45) -> pbga, havc, qoyq
                      tknk (41) -> ugml, padx, fwft
                      jptl (61)
                      ugml (68) -> gyxo, ebii, jptl
                      gyxo (61)
                      cntj (57)"""
    root = parse_program_tree(InputFromString(file_content))
    assert root.name == "tknk"
    assert root.total_weight() == 778
