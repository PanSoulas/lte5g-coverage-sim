from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import math



class AreaType(Enum):
    LARGE_CITY = "large_city"
    SMALL_MEDIUM_CITY = "small_medium_city"
    SUBURBAN = "suburban"
    OPEN = "open"


@dataclass
class HataFamilyConfig:
    area_type: AreaType 

class PropagationModel(ABC):
    VALID_RANGES: dict[str, tuple[float, float]] = {}

    def _validate_ranges(self, **param) -> None:
        for name, value in param.items():
            if name not in self.VALID_RANGES:
                continue
            low, high = self.VALID_RANGES[name]
            if not (low <= value <= high):
                raise ValueError(f"{name}={value} is out of range "
                                 f"[{low}, {high}] for {type(self).__name__}")
            
    @abstractmethod
    def path_loss(self, freq_mhz: float, height_bs: float, height_mobile: float, distance_km: float, config: object | None = None) -> float:
        pass
        
class OkumuraHata(PropagationModel):
    VALID_RANGES = {
        "freq_mhz": (150, 1500),
        "height_bs": (30, 200),
        "height_mobile": (1, 10),
        "distance_km": (1, 20)
    }

    def path_loss(self, freq_mhz: float, height_bs: float, height_mobile: float, distance_km: float, config: object | None = None) -> float:
        self._validate_ranges(freq_mhz = freq_mhz, 
                              height_bs = height_bs, 
                              height_mobile = height_mobile, 
                              distance_km = distance_km)
        if not isinstance(config, HataFamilyConfig):
            raise TypeError(f"OkumuraHata requires a HataFamilyConfig, got {type(config).__name__}")
        
        def a_hm(height_mobile: float, freq_mhz: float) -> float:
            if config.area_type == AreaType.LARGE_CITY:
                if freq_mhz >= 300:
                    return 3.2 * (math.log10(11.75 * height_mobile)) ** 2 - 4.97
                else:
                    return 8.29 * (math.log10(1.54 * height_mobile)) ** 2 - 1.1
            else:
                return (1.1 * math.log10(freq_mhz) - 0.7) * height_mobile - (1.56 * math.log10(freq_mhz) - 0.8)

        L_urban : float = (69.55 + 26.16 * math.log10(freq_mhz) - 13.82 * math.log10(height_bs) - a_hm(height_mobile, freq_mhz) +
                     (44.9 - 6.55 * math.log10(height_bs)) * math.log10(distance_km))
        
        if config.area_type == AreaType.SUBURBAN:
            L_suburban = L_urban - 2 * (math.log10(freq_mhz / 28)) ** 2 - 5.4
            return L_suburban
        elif config.area_type == AreaType.OPEN:
            L_open = L_urban - 4.78 * (math.log10(freq_mhz)) ** 2 + 18.33 * math.log10(freq_mhz) - 40.94
            return L_open

        return L_urban
