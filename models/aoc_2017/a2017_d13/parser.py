from models.common.io import InputReader

from .layered_firewall import FirewallLayer, LayeredFirewall


def parse_layered_firewall(input_reader: InputReader) -> LayeredFirewall:
    layers = {}
    for line in input_reader.readlines():
        parts = line.strip().split(":")
        layer_depth = int(parts[0])
        scanning_range = int(parts[1])
        layers[layer_depth] = FirewallLayer(scanning_range=scanning_range)
    return LayeredFirewall(layers)
