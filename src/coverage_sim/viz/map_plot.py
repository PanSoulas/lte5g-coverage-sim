import folium
from coverage_sim import sites


def rssi_to_color(rssi: float | None) -> str:
    if rssi is None:
        return '#808080'  # Gray : out of range
    elif rssi >= -70:
        return '#00FF00'  # Green : strong signal
    elif rssi >= -85:
        return '#FFFF00'  # Yellow : moderate signal
    else:
        return '#FF0000'  # Red : weak signal

def plot_map(site: sites.Site, grid: list[list[tuple[float, float]]], coverage: list[list[float | None]], output_file: str):
    m = folium.Map(location=[site.latitude, site.longitude], zoom_start=13)

    for i, row in enumerate(grid):
        for j, (lat, lon) in enumerate(row):
            loss = coverage[i][j]
            if loss is None:
                rssi = None
            else:
                rssi = site.tx_power_dbm - loss
            color = rssi_to_color(rssi)
            folium.CircleMarker(
                location=(lat, lon),
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)

    folium.Marker(
        location=(site.latitude, site.longitude),
        popup=f"Site: {site.name}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    m.save(output_file)
    return m
    