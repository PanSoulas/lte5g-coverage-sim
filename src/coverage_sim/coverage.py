from .sites import Site
from .models.base import PropagationModel
from geopy.distance import geodesic
from .models.base import OkumuraHata, HataFamilyConfig
from .models.cost231 import Cost231, CostFamilyConfig


def compute_coverage(site: Site, model: PropagationModel, grid: list[list[tuple[float, float]]], height_mobile: float) -> list[list[float | None]]:
    if isinstance(model, OkumuraHata):
        config = HataFamilyConfig(area_type=site.area_type)
    elif isinstance(model, Cost231):
        config = CostFamilyConfig(area_type=site.area_type)
    else:
        raise TypeError(f"Unsupported propagation model: {type(model).__name__}")
    
    result = []
    for row in grid:
        result_row = []
        for lat, lon in row:
            distance_km= geodesic((site.latitude, site.longitude), (lat, lon)).kilometers
            try:
                loss = model.path_loss(freq_mhz=site.freq_mhz,
                                    height_bs=site.height_bs,
                                    height_mobile=height_mobile,
                                    distance_km=distance_km,
                                    config=config)
            except ValueError:
                loss = None
            result_row.append(loss)
        result.append(result_row)

    return result

    