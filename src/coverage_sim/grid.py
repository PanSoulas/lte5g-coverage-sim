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


MAX_POINTS = 100000

def estimate_point_count(box: tuple, step_km: float) -> int:
    min_lat, min_lon, max_lat, max_lon = box
    height_km = geodesic(Point(min_lat, min_lon), Point(max_lat, min_lon)).kilometers
    width_km = geodesic(Point(min_lat, min_lon), Point(min_lat, max_lon)).kilometers
    row = int(height_km / step_km) + 1
    col = int(width_km / step_km) + 1
    return row * col

def generate_grid(box: tuple, step_km: float) -> list[list[tuple[float, float]]]:
    min_lat, min_lon, max_lat, max_lon = box

    count = estimate_point_count(box, step_km)
    if count > MAX_POINTS:
        raise ValueError(f"Grid produces {count} points, exceeding the {MAX_POINTS} limit. Consider increasing the step size or reducing site coverage area.")

    grid = []
    row_start = Point(min_lat, min_lon)
    while row_start.latitude <= max_lat:
        row = []
        point = row_start
        while point.longitude <= max_lon:
            row.append((point.latitude, point.longitude))
            point = geodesic(kilometers=step_km).destination(point, bearing=90)
        grid.append(row)
        row_start = geodesic(kilometers=step_km).destination(row_start, bearing=0)

    return grid