from dataclasses import dataclass
from .models.base import AreaType

@dataclass
class Site:
    name: str
    latitude: float
    longitude: float
    height_bs: float
    freq_mhz: float
    area_type: AreaType
    tx_power_dbm: float = 60.0  # Default transmit power in dBm