from ..layered_firewall import FirewallLayer, LayeredFirewall


def test_firewall_with_no_scanner_returns_minus_one_for_its_position():
    firewall = FirewallLayer()
    assert firewall.scanner_position_at_time(0) == -1


def test_scanner_starts_at_position_zero():
    assert FirewallLayer(scanning_range=1).scanner_position_at_time(0) == 0
    assert FirewallLayer(scanning_range=2).scanner_position_at_time(0) == 0


def test_scanner_travels_up_and_down_its_range_one_position_at_a_time():
    firewall = FirewallLayer(scanning_range=3)
    assert firewall.scanner_position_at_time(0) == 0
    assert firewall.scanner_position_at_time(1) == 1
    assert firewall.scanner_position_at_time(2) == 2
    assert firewall.scanner_position_at_time(3) == 1
    assert firewall.scanner_position_at_time(4) == 0
    assert firewall.scanner_position_at_time(5) == 1


def test_layered_firewall_keeps_track_of_all_layers_where_packet_collides_with_scanner():
    layer_0 = FirewallLayer(scanning_range=3)
    layer_1 = FirewallLayer(scanning_range=2)
    layer_4 = FirewallLayer(scanning_range=4)
    layer_6 = FirewallLayer(scanning_range=4)
    firewall = LayeredFirewall(layers={0: layer_0, 1: layer_1, 4: layer_4, 6: layer_6})
    assert list(firewall.packet_collisions()) == [(0, layer_0), (6, layer_6)]


def test_layered_firewall_informs_minimum_delay_to_avoid_collisions():
    firewall = LayeredFirewall(
        layers={
            0: FirewallLayer(scanning_range=3),
            1: FirewallLayer(scanning_range=2),
            4: FirewallLayer(scanning_range=4),
            6: FirewallLayer(scanning_range=4),
        }
    )
    assert firewall.minimum_delay_to_avoid_collisions() == 10
