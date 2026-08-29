from coverage_sim.sites import Site
from coverage_sim.grid import bounding_box, padding, generate_grid
from coverage_sim.models.base import AreaType, OkumuraHata
from coverage_sim.coverage import compute_coverage
from coverage_sim.viz.map_plot import plot_map

def main():
    site = Site(name="Demo Tower",
                latitude=39.665,
                longitude=20.8537,
                height_bs=50,
                freq_mhz=900,
                area_type=AreaType.LARGE_CITY,
                tx_power_dbm=60.0)
    
    box = bounding_box([site])
    padded_box = padding(box, padding_km=15)
    grid = generate_grid(padded_box, step_km=1)

    model = OkumuraHata()
    coverage = compute_coverage(site, model, grid, height_mobile=1.5)

    output_file = "demo_coverage_map.html"
    plot_map(site, grid, coverage, output_file)

    total_points = sum(len(row) for row in grid)
    valid_points = sum(1 for row in coverage for v in row if v is not None)
    print(f"Computed coverage for site '{site.name}' over {total_points} grid points.")
    print(f"{valid_points} points within the model's valid range.")
    print(f"Map saved to {output_file}")


if __name__ == "__main__":
    main()