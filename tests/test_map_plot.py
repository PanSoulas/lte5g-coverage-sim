from coverage_sim.viz.map_plot import rssi_to_color

def test_strong_signal_green():
    assert rssi_to_color(-70) == '#00FF00'

def test_moderate_signal_yellow():
    assert rssi_to_color(-71) == '#FFFF00'
    assert rssi_to_color(-85) == '#FFFF00'

def test_weak_signal_red():
    assert rssi_to_color(-86) == '#FF0000'

def test_none_is_gray():
    assert rssi_to_color(None) == '#808080'