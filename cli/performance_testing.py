"""Runs performance tests of model"""
import datetime as dt

import numpy as np

from beer_lambert_rt.model import run_model

ice_thickness = 1.5
snow_depth = 0.3
albedo = 0.8
sw_radiation = 100.
surface_temperature = -5.
sea_ice_concentration = 1.

def test(n, iterations=1):
    """Runs a single performance test for square array of size nxn"""
    use_distribution = True
    if n == 0:
        ice_thickness_a = ice_thickness
        snow_depth_a = snow_depth
        albedo_a = albedo
        sw_radiation_a = sw_radiation
        surface_temperature_a = surface_temperature
        sea_ice_concentration_a = sea_ice_concentration
    else:
        nn = n**2
        ice_thickness_a = np.full(nn, ice_thickness)
        snow_depth_a = np.full(nn, snow_depth)
        albedo_a = np.full(nn, albedo)
        sw_radiation_a = np.full(nn, sw_radiation)
        surface_temperature_a = np.full(nn, surface_temperature)
        sea_ice_concentration_a = np.full(nn, sea_ice_concentration)

    elapsed = []
    for i in range(iterations):
        start = dt.datetime.now()
        run_model(ice_thickness_a, snow_depth_a, albedo_a,
                  sw_radiation_a, surface_temperature_a,
                  sea_ice_concentration_a, use_distribution=use_distribution)
        end = dt.datetime.now()
        elapsed.append(end - start)
    print(f"Average Time Elapsed: {np.mean(elapsed)}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Tests performace of run_model")
    parser.add_argument("n", type=int)
    parser.add_argument("--iterations", "-i", type=int, default=1)
    args = parser.parse_args()
    test(args.n, iterations=args.iterations)
