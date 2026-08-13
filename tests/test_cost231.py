from coverage_sim.models.base import  AreaType
from coverage_sim.models.cost231 import Cost231, CostFamilyConfig
import pytest

def test_large_city_known_value():
    model = Cost231()
    config = CostFamilyConfig(area_type=AreaType.LARGE_CITY)
    result = model.path_loss(freq_mhz=1800,
                             height_bs=50,
                             height_mobile=1.5,
                             distance_km=5,
                             config=config)
    assert abs(result - 159.78) < 0.5

def test_out_of_range_raises():
    model = Cost231()
    config = CostFamilyConfig(area_type=AreaType.LARGE_CITY)
    with pytest.raises(ValueError):
        model.path_loss(freq_mhz=1800,
                        height_bs=50,
                        height_mobile=1.5,
                        distance_km=25,
                        config=config)

def test_invalid_config_type_raises():
    model = Cost231()
    with pytest.raises(TypeError):
        model.path_loss(freq_mhz=1800,
                        height_bs=50,
                        height_mobile=1.5,
                        distance_km=5,
                        config=None)
        