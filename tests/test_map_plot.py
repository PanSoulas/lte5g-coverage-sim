from coverage_sim.sites import Site
from coverage_sim.models.base import AreaType
from coverage_sim.viz.map_plot import rssi_to_color, site_color_map, site_icon_color_map

def test_strong_signal_green():
    assert rssi_to_color(-70) == '#00FF00'

def test_moderate_signal_yellow():
    assert rssi_to_color(-71) == '#FFFF00'
    assert rssi_to_color(-85) == '#FFFF00'

def test_weak_signal_red():
    assert rssi_to_color(-86) == '#FF0000'

def test_none_is_gray():
    assert rssi_to_color(None) == '#808080'

def test_site_color_map_assigns_distinct_colors():
    site1 = Site(name="A", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    site2 = Site(name="B", latitude=39.700, longitude=20.900, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    color_map = site_color_map([site1, site2])
    assert color_map["A"] != color_map["B"]

def test_site_icon_color_map_assigns_distinct_colors():
    site1 = Site(name="A", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    site2 = Site(name="B", latitude=39.700, longitude=20.900, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    icon_map = site_icon_color_map([site1, site2])
    assert icon_map["A"] != icon_map["B"]

