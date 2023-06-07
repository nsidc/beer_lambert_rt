"""Main model function and helper functions"""

from pathlib import Path
import warnings

import numpy as np
import xarray as xr
import pandas as pd

from beer_lambert_rt.transmission import (get_transmittance,
                                          transmission_open_water,
                                          modify_albedo)
from beer_lambert_rt.distributions import snow_ice_distribution
from beer_lambert_rt.constants import underice_flux2par, openwater_flux2par


def run_model(ice_thickness: float,
              snow_depth: float,
              albedo: float,
              sw_radiation: float,
              skin_temperature: float,
              sea_ice_concentration: float,
              pond_depth=0.,
              pond_fraction=None,
              use_distribution=True,
              nsnow_class=7.,
              max_snow_factor=3.,
              nice_class=15.,
              max_ice_factor=3.):
    """Runs Beer-Lambert RT model

    Arguments
    ---------
    :ice_thickness: (float) ice thickness in meters (scalar or array-like)
    :snow_depth: (float) snow depth in meters (scalar or array-like)
    :albedo: surface albedo [0-1] (scalar or array-like)
    :sw_radiation: Shortwave radiation (scalar or array-like)
    :skin_temperature: Skin temperature in degrees C (scalar or array-like)

    Keywords
    --------
    :sea_ice_concentration: Sea ice concentration [0-1] (scalar or array-like).  Default
                            is 1.
    :pond_depth: pond_depth in meters (scalar or array-like). Ignored if None.
    :pond_fraction: pond_fraction [0-1] (scalar or array-like). Only used if pond-depth
                    is not None. 
    :use_distribution: (boolean) Use ice_thickness and snow_depth to define snow and 
                       ice distribution. Default=True,
    :nsnow_class: Number of snow classes in snow depth distribution (scalar) Default=7.
    :max_snow_factor: Set maximum snow depth in distribution as max_snow_factor*snow_depth
                      Default=3.,
    :nice_class: **Not Used** Number of ice classes in ice thickness distribution (scalar) 
                 Default=15.
    :max_ice_factor: **Not Used** Set maximum ice thickness as max_ice_factor*ice_thickness
                     Default=3.

    :returns: TBD but PAR, Flux, ????
    """

    fixed_pond_depth = 0.
    fixed_pond_fraction = 0.
    
    # Prepare data - converts to numpy.ndarrays
    ice_thickness_a = check_isarray(ice_thickness)
    snow_depth_a = check_isarray(snow_depth)
    albedo_a = check_isarray(albedo)
    sw_radiation_a = check_isarray(sw_radiation)
    skin_temperature_a = check_isarray(skin_temperature)
    sea_ice_concentration_a = check_isarray(sea_ice_concentration)

    # Ponds are note included in the model yet so set to fixed zero values
    pond_depth_a = np.full_like(ice_thickness, fixed_pond_depth)
    pond_fraction_a = np.full_like(ice_thickness, fixed_pond_fraction)
    
    # Get input dimensions from ice_thickness.  All other inputs are expected
    # to have same dimensions.
    shape = ice_thickness_a.shape
    
    # Check all inputs have the same dimensions: except pond_depth and pond_fraction
    for arr in [ice_thickness_a, snow_depth_a, albedo_a, sw_radiation_a,
                skin_temperature_a, sea_ice_concentration_a,
                pond_depth_a, pond_fraction_a]:
        if arr.shape != shape:
            raise ValueError("One or more input arrays have mismatched shaped")


    zipped = zip(ice_thickness_a.flatten(),
                 snow_depth_a.flatten(),
                 albedo_a.flatten(),
                 sw_radiation_a.flatten(),
                 skin_temperature_a.flatten(),
                 sea_ice_concentration_a.flatten(),
                 pond_depth_a.flatten(),
                 pond_fraction_a.flatten())
    flux_list = []
    par_list = []
    for hice, hsnow, alb, swrad, stmp, sic, hpond, pfrac in zipped:
        flux, par = calculate_flux_and_par(hice, hsnow, alb, swrad,
                                           stmp, sic, hpond, pfrac,
                                           use_distribution=use_distribution)
        flux_list.append(flux)
        par_list.append(par)

    flux_arr = np.asarray(flux_list).reshape(shape)
    par_arr = np.asarray(par_list).reshape(shape)
    return flux_arr, par_arr


def check_isarray(x):
    """Checks that x is numpy.ndarray.  If not returns array."""
    return np.asarray([x]) if np.isscalar(x) else np.asarray(x)


def calculate_flux_and_par(
        ice_thickness: float,
        snow_depth: float,
        albedo: float,
        surface_flux: float,
        skin_temperature: float,
        sea_ice_concentration: float,
        pond_depth: float,
        pond_fraction: float,
        use_distribution=True,
        nsnow_class=7.,
        max_snow_factor=3.,
        nice_class=15.,
        max_ice_factor=3.):
    """Calculates flux and PAR for one input.  
    Function can be mapped to scalar, 1D and 2D arrays

    """

    for arr in [ice_thickness, snow_depth, albedo, surface_flux,
                skin_temperature, sea_ice_concentration, pond_depth, pond_fraction]:
        if not np.isscalar(arr):
            warnings.warn(f"One or more inputs is not scalar: shape: {arr.shape} "
                          "This may cause unexpected results", UserWarning)

    # Get ice cover albedo - check Key user guide
    ice_albedo = modify_albedo(albedo, sea_ice_concentration)
    
    # Calculate transmittance for ice fraction as distribution of single values
    ice_cover_transmittance = get_transmittance(ice_thickness, snow_depth,
                                                pond_depth, skin_temperature,
                                                use_distribution=use_distribution)
    ice_cover_transmittance = (1 - ice_albedo) * ice_cover_transmittance

    # Calculate flux for open water
    ow_transmittance = transmission_open_water()
    
    # Calculate total flux
    ice_swflux = surface_flux * ice_cover_transmittance
    ow_swflux = surface_flux * ow_transmittance

    ice_par = ice_swflux * underice_flux2par
    ow_par = ow_swflux * openwater_flux2par

    total_par = ((ice_par * sea_ice_concentration) +
                 (ow_par * (1 - sea_ice_concentration)))

    # Calculate mean flux
    total_flux = ((ice_swflux * sea_ice_concentration) +
                  (ow_swflux * (1 - sea_ice_concentration)))
                  
    return total_flux, total_par


def load_netcdf():
    testfile = Path("tests/test_data.nc")
    return xr.open_dataset(testfile)


def load_csv():
    testfile = Path("tests/test_data.csv")
    return pd.read_csv(testfile)


def main(test_format='nc', use_distribution=True):
    """Currently code to run model with dummy data

    This will be moved to the CLI directory"""

    if test_format == "nc":
        data = load_netcdf()
    elif test_format == "csv":
        data = load_csv()
    else:
        print(f"{test_format} is unknown test format!")

    result = run_model(
        data.ice_thickness,
        data.snow_depth,
        data.albedo,
        data.sw_radiation,
        data.surface_temperature,
        data.sea_ice_concentration,
        use_distribution=use_distribution
    )
    
    print(result)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Runs Beer Lambert RT model")
    parser.add_argument("--format", "-f", type=str, default="nc")
    parser.add_argument("--no_distribution", action='store_false')
        
    args = parser.parse_args()
    print(args)
    
    main(test_format=args.format, use_distribution=args.no_distribution)
