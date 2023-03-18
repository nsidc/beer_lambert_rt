import pytest

import beer_lambert_rt.transmission as transmission

from beer_lambert_rt.constants import (hssl_ice, hssl_dry_snow, hssl_wet_snow,
                                       k_ice, k_thin_ice,
                                       k_dry_snow, k_wet_snow, k_thin_wet_snow,
                                       i0_ice, i0_dry_snow, i0_wet_snow, i0_melt_ponds,
                                       albedo_open_water)

SURFACE_CONDITION = {
    "dry_snow": {"hice": 1.5, "hsnow": 0.3, "hpond": 0.0, "skin_temperature": -10.0},
    "wet_snow": {"hice": 1.5, "hsnow": 0.3, "hpond": 0.0, "skin_temperature": 0.0},
    "thin_wet_snow": {"hice": 1.5, "hsnow": 0.01, "hpond": 0.0, "skin_temperature": 0.0},
    "thick_bare_ice": {"hice": 1.5, "hsnow": 0.0, "hpond": 0.0, "skin_temperature": 0.0},
    "medium1_bare_ice": {"hice": 0.7, "hsnow": 0.0, "hpond": 0.0, "skin_temperature": 0.0},
    "medium2_bare_ice": {"hice": 0.3, "hsnow": 0.0, "hpond": 0.0, "skin_temperature": 0.0},
    "thin_bare_ice": {"hice": 0.09, "hsnow": 0.0, "hpond": 0.0, "skin_temperature": 0.0},
    "melt_pond": {"hice": 1.5, "hsnow": 0.0, "hpond": 0.3, "skin_temperature": 0.0},
    }


def test_green_edge_dry_snow():
    """Tests green_edge_hssl_snow for dry snow"""
    hsnow = 0.3
    skin_temperature = -10.
    expected = hssl_dry_snow
    result = transmission.green_edge_hssl_snow(hsnow, skin_temperature)
    assert expected == result

    
# def test_attenuation_coef_snow_dry_snow():
#     hsnow = 0.2
#     surface_temperature = -10.
#     expected = k_dry_snow
#     target = attenuation_coef_snow(hsnow, surface_temperature)
#     assert expected == target


# def test_attenuation_coef_snow_thick_wet_snow():
#     hsnow = 0.2
#     surface_temperature = 1.
#     expected = k_wet_snow
#     target = attenuation_coef_snow(hsnow, surface_temperature)
#     assert expected == target


# def test_attenuation_coef_snow_thin_wet_snow():
#     hsnow = 0.02
#     surface_temperature = 1.
#     expected = k_thin_snow
#     target = attenuation_coef_snow(hsnow, surface_temperature)
#     assert expected == target


# Add tests for snow transmittance
