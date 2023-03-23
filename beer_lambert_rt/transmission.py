"""
Functions and tools to calculate transmittance

These functions are a refactoring of Julienne Stroeve's Beer-Lambert 
sea ice radiative transfer model.  The original fundamental function 
get_f_att_snow of that model comprised if-elif-else statements to 
set parameters and calculate transmittance.  

Parameters are now set using a sequence of functions that use
np.piecewise and np.select to parameter values.  The main function
to calculate transmittance has been vectorized.  See the underice_light.ipynb
for an deeper explanation.

Parameters are selected for several cases:

- dry snow over ice
- wet snow over ice
- thin wet snow over ice - thin snow is hsnow < SSL_snow
- bare ice hice > 0.8
- bare ice 0.5 =< hice <= 0.8
- bare ice 0.1 < hice < 0.5
- bare ice hice < 0.1

"""

import numpy as np

from beer_lambert_rt.constants import (hssl_ice, hssl_dry_snow,
                                       hssl_wet_snow, hssl_thin_wet_snow,
                                       k_ice, k_thin_ice, k_dry_snow, k_wet_snow, k_thin_wet_snow,
                                       i0_ice, i0_dry_snow, i0_wet_snow, i0_melt_ponds,
                                       albedo_open_water)


def surface_type(hice, hsnow, hpond, surface_temperature):
    conditions = [
        (hsnow > hssl_wet_snow) & (surface_temperature > 0.),
        (hsnow <= hssl_wet_snow) & (surface_temperature > 0.),
        (hsnow > 0.) & (surface_temperature <= 0.),
        (hsnow == 0.) & (hice > hssl_ice),
        (hsnow == 0.) & (hice <= hssl_ice),
        (hpond > 0.),
    ]
    choices = [
        "Wet snow",
        "Thin wet snow",
        "Dry snow",
        "Bare ice",
        "Thin bare ice",
        "Melt pond",
    ]
    return np.select(conditions, choices)


def green_edge_hssl_snow(hsnow, surface_temperature):
    """Returns thickness of snow surface scattering layer following Green Edge study

    Add reference here

    hssl_snow = hssl_dry_snow
    if hsnow > hssl_wet_snow and surface_temperature > 0. hssl_wet_snow, zero otherwise
    """
    conditions = [
        (hsnow > 0.) & (surface_temperature <= 0.),
        (hsnow > hssl_wet_snow) & (surface_temperature > 0.),
        (hsnow <= hssl_wet_snow) & (surface_temperature > 0.),
        ]
    choices = [
        hssl_dry_snow,
        hssl_wet_snow,
        0.
        ]
    return np.select(conditions, choices)


def green_edge_hssl_ice(hice, hsnow, hpond):
    """
    Returns the the thickness of the ice surface scattering layer

    The thickness of the surface scattering layer is determined by a 
    piecewise function of hice, where

           | 0.0; hice < 0.5
    hssl = | hice/3. - 1./6.; 0.5 =< hice < 0.8
           | hssl_ice; hice > 0.8 
    
    I have no idea where this comes from.  Finding out.
    """
    ssl_slope = lambda hice: hice/3. - 1./6.
    conditions = [
        (hsnow > 0.),
        (hpond > 0.),
        (hsnow == 0.) & (hice < 0.5),
        (hsnow == 0.) & (hice >= 0.5) & (hice < 0.8),
        (hsnow == 0.) & (hice >= 0.8),
    ]
    choices = [
        0.0,
        0.0,
        0.0,
        ssl_slope,
        hssl_ice,
    ]
    return np.piecewise(hice, conditions, choices)


def cice_hssl_snow(hsnow, surface_temperature):
    """Placeholder for CICE style ssl parameterization"""
    raise NotImplemetedError


def cice_hssl_ice(hice, hsnow, hpond, surface_temperature):
    """Placeholder for CICE style ssl parameterization"""
    raise NotImplemetedError


def select_attenuation_ice(hice):
    """
    Returns attenuation coefficient of ice based on hice

    The attenuation coefficient of ice is dependent on the 
    ice thickness and the thickness of the surface scattering
    layer.  If ice thickness is less than or equal to the
    thickness of the surface scattering layer, the attenuation
    is set to a higher value.

           | k_thin_ice; hice < hssl_ice 
    kice = | 
           | k_ice; hice >= hssl_ice

    Parameters
    ----------
    :hice: scalar or arraylike
           ice thickness in meters

    :returns: scalar or arraylike with same dimensions as hice
    """
    conditions = [
        hice < hssl_ice,
        hice >= hssl_ice,
    ]
    choices = [
        k_thin_ice,
        k_ice,
    ]
    return np.select(conditions, choices)


def select_attenuation_snow(hsnow, surface_temperature):
    """Selects the attenuation coefficient for snow based on 
    snow depth and surface temperature"""
    conditions = [
        (hsnow > 0.) & (surface_temperature <= 0.),
        (hsnow > hssl_wet_snow) & (surface_temperature > 0.),
        (hsnow > 0.) & (hsnow <= hssl_wet_snow) & (surface_temperature > 0.),
    ]
    choices = [
        k_dry_snow,
        k_wet_snow,
        k_thin_wet_snow,
    ]
    return np.select(conditions, choices)


def select_surface_transmission(hice, hsnow, hpond, surface_temperature):
    """Selects i_0 based on surface type and temperature"""
    conditions = [
        hsnow == 0.,
        hpond > 0.,
        (hsnow > 0.) & (surface_temperature < 0.),
        (hsnow > 0.) & (surface_temperature >= 0.),
    ]
    choices = [
        i0_ice,
        i0_melt_ponds,
        i0_dry_snow,
        i0_wet_snow,
    ]
    return np.select(conditions, choices, None)


ssl_scheme_snow = {
    "green_edge": green_edge_hssl_snow,
    "cice": cice_hssl_snow,
    }
ssl_scheme_ice = {
    "green_edge": green_edge_hssl_ice,
    "cice": cice_hssl_ice,
    }


def transmission_open_water():
    """Returns transmittance for open water"""
    return 1 - albedo_open_water


def calculate_transmittance(hice, hsnow, hpond, surface_temperature,
                            ssl_parameterization="green_edge"):
    """Returns transmittance for a snow-ice-pond column_stack

    :hice: float - scalar or ndarray - ice thickness in m
    :hsnow: float - scalar or ndarray - snow depth in m
    :hpond: float - scalar or ndarray - pond depth in m.  If hpond > 0, hsnow must
            be zero.  Raises an ValueError exception.
    :surface_temperature: float - scalar or ndarray - surface temperature in deg. C

    :returns: bulk transmittance with same dimensions as input.

    Parameters are selected based on ice thickness, snow depth, pond depth,
    and skin temperature.  Parameter selection routines adjust surface scattering layer 
    thickness, such that h - hssl in esnow and eice evaluate to 1 when hsnow or hice
    is zero.  The surface transmission parameter i0 is set accordingly.

    If hice is zero, an exception is raised.
    If hsnow > 0 and hpond > 0. an exeption is raised.  Model does not allow for ponds
    on snow.
    """
    if (hice <= 0).any():
        raise ValueError("One or more hice is zero.  This condition is not allowed")

    if ((hsnow > 0.) & (hpond > 0)).any():
        raise ValueError("One or more hsnow > 0. and hpond > 0.!")
    
    i0 = select_surface_transmission(hice, hsnow, hpond, surface_temperature)
    hssl_ice = green_edge_hssl_ice(hice, hsnow, hpond)
    hssl_snow = green_edge_hssl_snow(hsnow, surface_temperature)
    kice = select_attenuation_ice(hice)
    ksnow = select_attenuation_snow(hsnow, surface_temperature)

    # Evaluates to zero when hsnow is zero
    esnow = np.exp(-1. * ksnow * (hsnow - hssl_snow))

    eice = np.exp(-1. * kice * (hice - hssl_ice))

    return i0 * esnow * eice
