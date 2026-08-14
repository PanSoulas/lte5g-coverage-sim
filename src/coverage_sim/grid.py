from .sites import Site
from geopy.distance import geodesic
from geopy import Point


def padding(box: tuple, padding_km: float) -> tuple:
    min_lat, min_lon, max_lat, max_lon = box

    north_edge = geodesic(kilometers=padding_km).destination(Point(max_lat, min_lon), bearing=0).latitude
    south_edge = geodesic(kilometers=padding_km).destination(Point(min_lat, min_lon), bearing=180).latitude

    east_edge = geodesic(kilometers=padding_km).destination(Point(max_lat, max_lon), bearing=90).longitude    
    west_edge = geodesic(kilometers=padding_km).destination(Point(min_lat, min_lon), bearing=270).longitude
    return (south_edge, west_edge, north_edge, east_edge)

def bounding_box(sites: list[Site]) -> tuple:
    latitudes = [s.latitude for s in sites]
    longitudes = [s.longitude for s in sites]
    return (min(latitudes), min(longitudes), max(latitudes), max(longitudes))
