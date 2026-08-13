from coverage_sim.models.base import  OkumuraHata, HataFamilyConfig, AreaType
import pytest

def test_large_city_known_value():
    model = OkumuraHata()
    config = HataFamilyConfig(area_type=AreaType.LARGE_CITY)
    result = model.path_loss(freq_mhz=900,
                             height_bs=50,
                             height_mobile=1.5,
                             distance_km=5,
                             config=config)
    assert abs(result - 146.95) < 0.5

def test_out_of_range_raises():
    model = OkumuraHata()
    config = HataFamilyConfig(area_type=AreaType.LARGE_CITY)
    with pytest.raises(ValueError):
        model.path_loss(freq_mhz=900,
                        height_bs=50,
                        height_mobile=1.5,
                        distance_km=25,
                        config=config)
        
def test_invalid_config_type_raises():
    model = OkumuraHata()
    with pytest.raises(TypeError):
        model.path_loss(freq_mhz=900,
                        height_bs=50,
                        height_mobile=1.5,
                        distance_km=5,
                        config=None)