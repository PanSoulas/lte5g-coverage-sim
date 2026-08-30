from coverage_sim.sites import Site
from coverage_sim.grid import bounding_box, padding, generate_grid
from coverage_sim.models.base import AreaType, OkumuraHata
from coverage_sim.coverage import compute_coverage
from coverage_sim.viz.map_plot import plot_map
from coverage_sim.models.cost231 import Cost231
import argparse

def cli():
    parser = argparse.ArgumentParser(description="LTE/5G coverage prediction simulator")
    parser.add_argument("--lat", type=float, required=True, help="Site Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Site Longitude")
    parser.add_argument("--area-type", type=AreaType, required=True, choices=list(AreaType), help="Area type of the site")
    parser.add_argument("--model", type=str, required=True, choices=["hata", "cost231"], help="Propagation model to use")
    parser.add_argument("--height-bs", type=float, required=True, help="Base station antenna height (m)")
    parser.add_argument("--freq", type=float, required=True, help="Frequency (MHz)")
    parser.add_argument("--padding-km", type=float, default=15.0, help="Grid padding around site (km), default 15.0")
    parser.add_argument("--step-km", type=float, default=1.0, help="Grid resolution (km), default 1.0")
    parser.add_argument("--height-mobile", type=float, default=1.5, help="Receiver height (m), default 1.5")
    parser.add_argument("--tx-power", type=float, default=60.0, help="Transmit power (dBm), default 60.0")
    
    parser.add_argument("--output", type=str, default="coverage_map.html", help="Output HTML file path")

    args = parser.parse_args()
    return args

def main():
    args = cli()
    site = Site(name="Site",
                latitude=args.lat,
                longitude=args.lon,
                height_bs=args.height_bs,
                freq_mhz=args.freq,
                area_type=args.area_type,
                tx_power_dbm=args.tx_power)
    if args.model == "hata":
        model = OkumuraHata()
       
    elif args.model == "cost231":
        model = Cost231()


    box = bounding_box([site])
    padded_box = padding(box, padding_km=args.padding_km)
    grid = generate_grid(padded_box, step_km=args.step_km)
    coverage = compute_coverage(site, model, grid, height_mobile=args.height_mobile)

    output_file = args.output
    plot_map(site, grid, coverage, output_file)

    total_points = sum(len(row) for row in grid)
    valid_points = sum(1 for row in coverage for v in row if v is not None)
    print(f"Computed coverage for site '{site.name}' over {total_points} grid points.")
    print(f"{valid_points} points within the model's valid range.")
    print(f"Map saved to {output_file}")

if __name__ == "__main__":
    main()