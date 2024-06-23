from models.common.io import IOHandler
from .ip_parser import IpParser


def aoc_2016_d7(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2016, 7, "Internet Protocol Version 7")
    num_ips_that_support_tls = 0
    num_ips_that_support_ssl = 0
    for line in io_handler.input_reader.readlines():
        ip_parser = IpParser(line.strip())
        if ip_parser.supports_tls():
            num_ips_that_support_tls += 1
        if ip_parser.supports_ssl():
            num_ips_that_support_ssl += 1
    print(f"Part 1: Number of IPs that support TLS: {num_ips_that_support_tls}")
    print(f"Part 2: Number of IPs that support SSL: {num_ips_that_support_ssl}")
