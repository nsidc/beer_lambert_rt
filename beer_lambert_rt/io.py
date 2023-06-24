"""Loaders for data"""

from pathlib import Path
import datetime as dt
import os
import socket
import platform
import re
import inspect

import xarray as xr
import pandas as pd

import beer_lambert_rt
import beer_lambert_rt.constants as constants


TESTPATH = Path("tests")

EXPECTED_VARIABLES = [
    "ice_thickness",
    "snow_depth",
    "albedo",
    "sw_radiation",
    "surface_temperature",
    "sea_ice_concentration",
    "pond_depth",
    ]


flux_attrs = {
    "standard_name": "downwelling_shortwave_flux_in_sea_water_at_sea_ice_base",
    "units": "W m-2",
}
par_attrs = {
    "standard_name": "downwelling_photosynthetic_photon_spherical_irradiance_in_sea_water_at_sea_ice_base",
    "units": "mol m-2 s-1",
}


def load_netcdf(filepath):
    ds = xr.open_dataset(filepath)
    if not all([var in ds.data_vars for var in EXPECTED_VARIABLES]):
        raise KeyError(f"Input file {filepath} must contain variables: "
                       f"{', '.join(EXPECTED_VARIABLES)}")
    return ds


def load_csv(filepath):
    """Loads a csv file into a pandas dataframe and returns it as an
    xarray dataset"""
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    if not all([var in df.columns for var in EXPECTED_VARIABLES]):
        raise KeyError(f"Input file {filepath} must contain columns: "
                       f"{', '.join(EXPECTED_VARIABLES)}")
    return df.to_xarray()


def test_datapath(test_format='nc'):
    """Loads test data in a specific format"""
    if test_format == "nc":
        return TESTPATH / f"test_data.{test_format}"
    elif test_format == "csv":
        return TESTPATH / f"test_data.{test_format}"
    else:
        raise ValueError(f"{test_format} is unknown test format!")


def load_data(filepath):
    """Loads input data"""
    if filepath.suffix == ".nc":
        data = load_netcdf(filepath)
    elif filepath.suffix == ".csv":
        data = load_csv(filepath)
    else:
        raise ValueError(f"{filepath} is unknown format!  Expects netcdf or csv")
    return data


def write_results(outpath):
    """Writes results to output file.

    File type is assumed same as input"""
    return


def make_outpath(input_path, outformat):
    """Makes output path name"""
    return input_path.parent / f"{input_path.name}.flux_and_par.{outformat}"


def make_global_attrs(source_file):
    """Returns a dict object for netcdf global attrs

    Model parameters are written to the attributes, 
    along with source file, date created and user name of
    creator
    """
    global_attrs = {
        'source_file': str(source_file.absolute()),
        'created': dt.datetime.now().isoformat(),
        'created_by': os.getlogin(),
        'machine': socket.gethostname(),
        'platform': platform.platform(),
        'model': 'beer_lambert_rt',
        'model_version': beer_lambert_rt.__version__ if hasattr(beer_lambert_rt, '__version__') else '',
    }
    constants_dict = constants_to_dict()
    return {**global_attrs, **constants_dict}


def make_netcdf(flux, par, dims, coords, source_file):
    """Generates a netcdf file"""
    global_attrs = make_global_attrs(source_file)
    ds = xr.Dataset(
        {
            'sw_flux': (dims, flux, flux_attrs),
            'par': (dims, par, par_attrs),
        },
        coords = coords,
        attrs = global_attrs,
    )
    return ds


def ismyconstant(member):
    """Returns True if member of constants module is constant"""
    isdunder = lambda x: re.match('__.*__', x)
    if not isdunder(member[0]) and not inspect.ismodule(member[1]):
        return True
    else:
        return False

def constants_to_dict():
    """Returns a dict of constants"""
    return {member[0]: member[1] for member in inspect.getmembers(constants) if ismyconstant(member)}
