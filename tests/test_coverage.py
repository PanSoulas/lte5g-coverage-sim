from geopy.distance import geodesic
from coverage_sim.sites import Site
from coverage_sim.models.base import AreaType, HataFamilyConfig, OkumuraHata
from coverage_sim.models.cost231 import Cost231
from coverage_sim.coverage import compute_coverage
import pytest

def test_known_point_matches_direct_model_call():
    site = Site(name="TestSite", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    target_lat, target_lon = 39.700, 20.900
    grid = [[(target_lat, target_lon)]]

    model = OkumuraHata()
    coverage = compute_coverage(site, model, grid, height_mobile=1.5)

    distance_km = geodesic((site.latitude, site.longitude), (target_lat, target_lon)).kilometers
    config = HataFamilyConfig(area_type=AreaType.LARGE_CITY)
    expected = model.path_loss(freq_mhz=900, height_bs=50, height_mobile=1.5, distance_km=distance_km, config=config)

    assert coverage[0][0] == expected

def test_out_of_range_point() -> None:
    site = Site(name="TestSite", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    target_lat, target_lon = 0.1, 0.2
    grid = [[(target_lat, target_lon)]]

    model = OkumuraHata()
    coverage = compute_coverage(site, model, grid, height_mobile=1.5)

    assert coverage[0][0] is None

def test_usupported_model():
    site = Site(name="TestSite", latitude=39.665, longitude=20.8537, height_bs=50, freq_mhz=900, area_type=AreaType.LARGE_CITY)
    target_lat, target_lon = 39.700, 20.900
    grid = [[(target_lat, target_lon)]]
    model = None

    with pytest.raises(TypeError):
        compute_coverage(site, model, grid, height_mobile=1.5)