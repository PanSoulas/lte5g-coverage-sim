from coverage_sim.sites import Site
from coverage_sim.models.base import AreaType
from coverage_sim.coverage import best_server

def test_best_server_known_values():
    site1 = Site(name="A", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY, tx_power_dbm=60.0)
    site2 = Site(name="B", latitude=39.700, longitude=20.900, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY, tx_power_dbm=60.0)

    grid_a = [[140.0, 150.0], [145.0, None]]
    grid_b = [[160.0, 130.0], [None, 155.0]]

    result = best_server([site1, site2], [grid_a, grid_b])

    assert result[0][0] == ("A", -80.0)
    assert result[0][1] == ("B", -70.0)
    assert result[1][0] == ("A", -85.0)
    assert result[1][1] == ("B", -95.0)

def test_best_server_no_coverage_anywhere():
    site1 = Site(name="A", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY, tx_power_dbm=60.0)
    site2 = Site(name="B", latitude=39.700, longitude=20.900, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY, tx_power_dbm=60.0)

    grid_a = [[None]]
    grid_b = [[None]]

    result = best_server([site1, site2], [grid_a, grid_b])

    assert result[0][0] == (None, None)