from models.common.io import InputFromString
from ..parser import parse_storage_nodes


def test_parse_storage_nodes():
    file_content = """root@ebhq-gridcenter# df -h
                      Filesystem              Size  Used  Avail  Use%
                      /dev/grid/node-x0-y0     92T   68T    24T   73%
                      /dev/grid/node-x0-y1     88T   73T    15T   82%"""
    nodes = list(parse_storage_nodes(InputFromString(file_content)))
    assert nodes[0].size, nodes[0].used == (92, 68)
    assert nodes[1].size, nodes[1].used == (88, 73)
