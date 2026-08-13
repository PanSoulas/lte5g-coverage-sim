from dataclasses import dataclass
from .base import AreaType, PropagationModel
import math

@dataclass
class CostFamilyConfig:
    area_type: AreaType

class Cost231(PropagationModel):
    VALID_RANGES = {
        "freq_mhz": (1500, 2000),
        "height_bs": (30, 200),
        "height_mobile": (1, 10),
        "distance_km": (1, 20)
    }

    def path_loss(self, freq_mhz, height_bs, height_mobile, distance_km, config = None):
        self._validate_ranges(freq_mhz=freq_mhz,
                              height_bs=height_bs,
                              height_mobile=height_mobile,
                              distance_km=distance_km)
        if not isinstance(config, CostFamilyConfig):
            raise TypeError(f"Cost231 requires a CostFamilyConfig, got {type(config).__name__}")

        def a_hm(height_mobile, freq_mhz):
            if config.area_type == AreaType.LARGE_CITY:
                return 3.2 * (math.log10(11.75 * height_mobile)) ** 2 - 4.97
            else:
                return (1.1 * math.log10(freq_mhz) - 0.7) * height_mobile - (1.56 * math.log10(freq_mhz) - 0.8)
        
        if config.area_type == AreaType.LARGE_CITY:
            C_M = 3
            L = 46.3 + 33.9 * (math.log10(freq_mhz)) - 13.82 * math.log10(height_bs) - a_hm(height_mobile, freq_mhz) + (44.9 - 6.55 * math.log10(height_bs)) * math.log10(distance_km) + C_M
        else:
            L = 46.3 + 33.9 * (math.log10(freq_mhz)) - 13.82 * math.log10(height_bs) - a_hm(height_mobile, freq_mhz) + (44.9 - 6.55 * math.log10(height_bs)) * math.log10(distance_km)

        return L
    
