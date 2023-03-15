"""Functions and tools to calculate transmittance"""

import numpy as np

from beer_lambert_rt.constants import (hssl_ice, hssl_dry_snow, hssl_wet_snow,
                                       k_ice, k_dry_snow, k_wet_snow, k_thin_snow,
                                       i0_ice, i0_dry_snow, i0_wet_snow, i0_melt_ponds,
                                       albedo_open_water)


def attenuation_coef_snow(hsnow, surface_temperature):
    """Returns the attenuation coeficient for snow based on
       snow depth and whether snow is wet or dry based on
       surface temperature.

    :hsnow: snow depth in m
    :surface_temperature: snow surface temperature in degree C

    :return: attenuation coeficient
    """
    ksnow = k_dry_snow
    if surface_temperature > 0.:
        if hsnow <= hssl_wet_snow:
            ksnow = k_thin_snow
        else:
            ksnow = k_wet_snow
    return ksnow


def adjust_hsnow(hsnow, surface_temperature):
    """Adjusts hsnow to account for surface scattering layer
    based on temperature.

    :hsnow: snow depth in m
    :surface_temperature: snow surface temperature in degree C

    :return: attenuation coeficient
    """
    hsnow_adj = hsnow
    if surface_temperature > 0.:
        if hsnow > hssl_wet_snow:
            hsnow_adj = hsnow - hssl_wet_snow
    return hsnow_adj


def transmission_open_water():
    """Returns transmittance for open water"""
    return 1 - albedo_open_water


def transmission_pond(hice):
    """Returns transmittance for a pond

    :hice: ice thickness in m
    
    :returns: pond transmittance
    """
    eice = np.exp(-1. * k_ice * hice)
    return i0_melt_ponds * (1-albedo_pond) * eice


def transmission_coef_snow(hsnow, surface_temperature):
    """Returns transmission coefficient for snow based on
    snow depth and surface temperature

    :hsnow: snow depth in m
    :surface_temperature: snow surface temperature in degree C

    :return: transmission coeficient.
    """
    raise NotImplemetedError("Fix this now")


def transmission_snow_covered_ice(hsnow, hice, albedo, surface_temperature):
    """Returns transmittance for snow covered ice.

    :hsnow: float, scalar or ndarray of snow depth in m
    :hice: float, scalar or ndarray of ice thickness in m
    :albedo: float, surface albedo
    :surface_temperature: float, scalar or ndarray of surface temperature C

    :returns: scalar or ndarray of floats of transmittance
    """
    ksnow = attenuation_coef_snow(hsnow, surface_temperature)
    hsnow_adj = adjust_hsnow(hsnow, surface_temperature)
    i0_snow = transmission_coef_snow(hsnow, surface_temperature)
    esnow = np.exp(-1. * ksnow * hsnow_adj)
    eice = np.exp(-1. * k_ice * hice)
    return i0_snow * (1-albedo) * esnow * eice


"""
There are several cases:

- dry snow over ice - no SSL
- wet snow over ice - 3 cm SSL - wet snow defined by surface_temperature > 0.
- thin wet snow over ice - hsnow < SSL_snow
- bare ice > 0.8
- bare ice 0.5 =< hice <= 0.8
- bare ice 0.1 < hice < 0.5
- bare ice hice < 0.1
"""

def select_transmission(hice, hsnow, hpond, surface_temperature):
    """Returns trasnmission function based on snow depth, ice thickness
       and surface temperature

    Distinguishes between wet and dry snow based on surface temperature
    Shallow and deep snow packs are based whether or not snow is deeper than snow SSL_snow
    
    :hice: float - scalar or ndarray - ice thickness in m
    :hsnow: float - scalar or ndarray - snow depth in m
    :hpond: float - scalar or ndarray - pond depth in m.  If hpond > 0, hsnow must
            be zero.  Raises an ValueError exception.
    :surface_temperature: float - scalar or ndarray - surface temperature in deg. C

    """
    conditions_lut = {
        "dry_snow": (hsnow > 0.) & (surface_temperature <= 0.),
        "shallow_wet_snow": (hsnow > 0.) & (hsnow <= hssl_wet_snow) & (surface_temperature > 0.),
        "deep_wet_snow": (hsnow > hssl_wet_snow) & (surface_temperature > 0.),
        "thick_ice": (hsnow == 0.) & (hice > 0.8),
        "medium_ice1": (hsnow == 0.) & (hice >= 0.5) & (hice <= 0.8),
        "medium_ice2": (hsnow == 0.) & (hice >= 0.1) & (hice < 0.5),
        "thin_ice": (hsnow == 0.) & (hice < 0.1),
        }
    condition = conditions_lut.values()
    choice = conditions_lut.keys()
    return np.select(condition, choice, None)

     
def calculate_transmission(hice, hsnow, hpond, surface_temperature):
    """Returns transmittance for a snow-ice-pond column_stack

    :hice: float - scalar or ndarray - ice thickness in m
    :hsnow: float - scalar or ndarray - snow depth in m
    :hpond: float - scalar or ndarray - pond depth in m.  If hpond > 0, hsnow must
            be zero.  Raises an ValueError exception.
    :surface_temperature: float - scalar or ndarray - surface temperature in deg. C

    :returns: bulk transmittance with same dimensions as input.

    N.B. All inputs must be same shape.
    """

    #if not (hice.shape == hsnow.shape == hpond.shape):
    #    raise ValueError("Expects hice, hsnow and hpond to be same shape")

    if (hsnow > 0.):
        if (surface_temperature > 0.):
            if (hsnow <= hssl_wet_snow):
                print("Thin Wet snow covered ice")
            else:
                print("Thick wet snow covered ice")
        else:
            print("Dry snow covered ice")
#    else:
#        if (hice < 0.1):
#            print("Thin bare ice")
#        elif (hice >= 0.1) & (hice <
#    elif (hsnow > hssl_wet_snow)
