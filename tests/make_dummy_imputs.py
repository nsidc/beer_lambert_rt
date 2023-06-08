"""Generate dummy input files"""

from pathlib import Path

import numpy as np
import xarray as xr
import pandas as pd

TESTPATH = Path('tests')

ice_thickness = np.array([1.5, 1., 0.7, 0.5])
snow_depth = np.array([0.3, 0.5, 1.0, 0.2])
pond_depth = np.array([0.3, 0.2, 0.5, 0.1])
sw_radiation = np.array([94., 100., 80., 120.])
albedo = np.array([0.8, 0.9, 0.85, 0.7])
sea_ice_concentration = np.array([1., 0.6, 0.86, 0.2])
surface_temperature = np.array([0., -1.5, -20., 0.])

ds = xr.Dataset(
    {
        'ice_thickness': (('x', 'y'), ice_thickness.reshape(2, 2)),
        'snow_depth': (('x', 'y'), snow_depth.reshape(2, 2)),
        'pond_depth': (('x', 'y'), pond_depth.reshape(2, 2)),
        'sw_radiation': (('x', 'y'), sw_radiation.reshape(2, 2)),
        'albedo': (('x', 'y'), albedo.reshape(2, 2)),
        'sea_ice_concentration': (('x', 'y'), sea_ice_concentration.reshape(2, 2)),
        'surface_temperature': (('x', 'y'), surface_temperature.reshape(2, 2)),
    },
    coords = {
        'x': [1., 2.],
        'y': [1., 2.],
        }
)

df = pd.DataFrame(
    {
        'ice_thickness': ice_thickness,
        'snow_depth': snow_depth,
        'pond_depth': pond_depth,
        'sw_radiation': sw_radiation,
        'albedo': albedo,
        'sea_ice_concentration': sea_ice_concentration,
        'surface_temperature': surface_temperature,
    },
    index=pd.date_range('2020-06-01', periods=ice_thickness.size, freq='D')
)

ds.to_netcdf(TESTPATH / "test_data.nc")
df.to_csv(TESTPATH / "test_data.csv")
