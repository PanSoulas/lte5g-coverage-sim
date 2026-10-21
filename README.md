# LTE/5G Coverage Prediction Simulator

A Python tool that predicts cellular signal coverage around one or more base stations using empirical path loss models (**Okumura-Hata** and **COST-231 Hata**) and renders the result as an interactive map.

![Single-site coverage map](docs/images/single_site.png)

## Features

- **Two propagation models** behind a shared interface: Okumura-Hata (150-1500 MHz) and COST-231 Hata (1500-2000 MHz)
- **Four area types**: large city, small/medium city, suburban, open
- **Strict validity checking**: inputs outside a model's valid range raise an error instead of silently returning a misleading number
- **Geodesic grid generation** over a padded bounding box, with a safety cap on total grid points
- **Multi-site "best server" maps**: for every grid point, the site with the strongest received signal wins
- **Interactive map output** (folium/Leaflet) saved as a standalone HTML file
- **Command-line interface** for single-site runs
- **Automated tests and CI** (Python 3.12 and 3.14)

## Example output

| Single site (RSSI-colored) | Two sites (best server) |
|---|---|
| ![Single site](docs/images/single_site.png) | ![Best server](docs/images/best_server.png) |

Single-site colors show signal strength (green = strong, yellow = moderate, red = weak, gray = outside the model's valid range). In the best-server map, each color marks the territory of one site.

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/PanSoulas/lte5g-coverage-sim.git
cd lte5g-coverage-sim
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

## Usage

### Command line (single site)

```bash
python -m coverage_sim.cli \
  --lat 39.665 --lon 20.8537 \
  --area-type large_city \
  --model hata \
  --height-bs 50 --freq 900 \
  --output coverage_map.html
```

| Argument | Description | Default |
|---|---|---|
| `--lat`, `--lon` | Site coordinates | required |
| `--height-bs` | Base station antenna height (m) | required |
| `--freq` | Frequency (MHz) | required |
| `--area-type` | `large_city`, `small_medium_city`, `suburban`, `open` | required |
| `--model` | `hata` or `cost231` | required |
| `--tx-power` | Transmit power / EIRP (dBm) | 60.0 |
| `--height-mobile` | Receiver height (m) | 1.5 |
| `--padding-km` | Grid padding around the site (km) | 15.0 |
| `--step-km` | Grid resolution (km) | 1.0 |
| `--output` | Output HTML file | `coverage_map.html` |

Open the generated HTML file in any browser.

### Demo script

```bash
python examples/single_site_demo.py
```

### Python API (multi-site best server)

```python
from coverage_sim.sites import Site
from coverage_sim.grid import bounding_box, padding, generate_grid
from coverage_sim.models.base import AreaType, OkumuraHata
from coverage_sim.coverage import compute_coverage, best_server
from coverage_sim.viz.map_plot import plot_best_server_map

site_a = Site(name="Tower A", latitude=39.665, longitude=20.8537, height_bs=50,
              freq_mhz=900, area_type=AreaType.LARGE_CITY, tx_power_dbm=60.0)
site_b = Site(name="Tower B", latitude=39.700, longitude=20.900, height_bs=50,
              freq_mhz=900, area_type=AreaType.LARGE_CITY, tx_power_dbm=60.0)
sites = [site_a, site_b]

grid = generate_grid(padding(bounding_box(sites), 15), step_km=1)

model = OkumuraHata()
coverage = [compute_coverage(s, model, grid, height_mobile=1.5) for s in sites]

best = best_server(sites, coverage)
plot_best_server_map(sites, grid, best, "best_server.html")
```

## How it works

```
Site(s) ──► bounding box + padding ──► rectangular lat/lon grid
                                              │
              propagation model ──► path loss per grid point (per site)
                                              │
                         RSSI = tx_power - path_loss
                                              │
                    best server per cell (multi-site) ──► folium map
```

### Models

**Okumura-Hata**

```
L = 69.55 + 26.16*log10(f) - 13.82*log10(h_BS) - a(h_m)
    + (44.9 - 6.55*log10(h_BS)) * log10(d)
```

with the mobile antenna correction `a(h_m)` depending on city size, plus suburban and open-area corrections applied on top of the urban result.

**COST-231 Hata**

```
L = 46.3 + 33.9*log10(f) - 13.82*log10(h_BS) - a(h_m)
    + (44.9 - 6.55*log10(h_BS)) * log10(d) + C_M
```

where `C_M = 3 dB` for large cities and `0 dB` otherwise.

### Valid ranges (enforced)

| Parameter | Okumura-Hata | COST-231 |
|---|---|---|
| Frequency | 150-1500 MHz | 1500-2000 MHz |
| Base station height | 30-200 m | 30-200 m |
| Mobile height | 1-10 m | 1-10 m |
| Distance | 1-20 km | 1-20 km |

Grid points outside the distance range (very close to the site, or in the far corners of the padded grid) are marked as "no data" rather than computed.

## Project structure

```
lte5g-coverage-sim/
├── src/coverage_sim/
│   ├── models/
│   │   ├── base.py          # PropagationModel interface, AreaType, Okumura-Hata
│   │   └── cost231.py       # COST-231 Hata model
│   ├── sites.py             # Site dataclass
│   ├── grid.py              # bounding box, geodesic padding, grid generation
│   ├── coverage.py          # compute_coverage, best_server
│   ├── viz/map_plot.py      # folium map rendering
│   └── cli.py               # command-line interface
├── tests/
├── examples/single_site_demo.py
└── .github/workflows/tests.yml
```

## Testing

```bash
pytest -v
```

Reference values for the propagation models were computed by hand and independently verified. Tests also cover out-of-range handling, invalid configuration types, the coverage/model wiring, best-server selection (including the no-coverage case), and map color logic. CI runs the suite on Python 3.12 and 3.14 for every pull request.

## Design decisions

- **Rectangular grid instead of radial rings**, so every site is evaluated on the same points. This is what makes best-server comparison a simple per-cell operation.
- **Fail loudly on out-of-range inputs.** A prediction tool that silently returns plausible-looking wrong numbers is worse than one that refuses.
- **Model-specific config objects** (`HataFamilyConfig`, `CostFamilyConfig`) keep the shared model interface honest for future models that don't use area types.
- **Geodesic distances (geopy)** rather than flat-earth approximations.

## Limitations

- Empirical models only: no terrain, buildings, or clutter data
- The models are valid up to 2000 MHz, so higher 5G bands (e.g. 3.5 GHz) are out of scope
- "RSSI" here is simply `tx_power - path_loss`, with no antenna gain, cable loss, or fading margins
- The CLI handles a single site; multi-site maps currently go through the Python API

## Roadmap

- Terrain integration (SRTM elevation data)
- Model comparison overlays and frequency-sweep plots
- SINR / interference layer
- Validation against real tower locations (e.g. OpenCelliD)
- Multi-site support in the CLI

## License

<add your license here>
