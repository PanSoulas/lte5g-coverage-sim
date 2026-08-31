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
    

PALETTE = ['#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c']
ICON_PALETTE = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black']

def site_icon_color_map(sites: list[sites.Site]) -> dict[str, str]:
    return {site.name: ICON_PALETTE[i % len(ICON_PALETTE)] for i, site in enumerate(sites)}

def site_color_map(sites: list[sites.Site]) -> dict[str, str]:
    return {site.name: PALETTE[i % len(PALETTE)] for i, site in enumerate(sites)}

def plot_best_server_map(site_list: list[sites.Site], grid: list[list[tuple[float, float]]], best_server_grid: list[list[tuple[str | None, float | None]]], output_file: str):
    avg_lat = sum(s.latitude for s in site_list) / len(site_list)
    avg_lon = sum(s.longitude for s in site_list) / len(site_list)
    best_m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)
    color_map = site_color_map(site_list)


    for i, row in enumerate(grid):
        for j, (lat, lon) in enumerate(row):
            site_name, rssi = best_server_grid[i][j]
            if site_name is None:
                color = '#808080'
            else:
                color = color_map[site_name]
            folium.CircleMarker(
                location=(lat, lon),
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(best_m)

    icon_color_map = site_icon_color_map(site_list)
    for site in site_list:
        folium.Marker(
            location=(site.latitude, site.longitude),
            popup=f"Site: {site.name}",
            icon=folium.Icon(color=icon_color_map[site.name], icon='info-sign')
        ).add_to(best_m)
    best_m.save(output_file)
    return best_m