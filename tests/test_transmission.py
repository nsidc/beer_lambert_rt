import pytest

from beer_lambert_rt.transmission import adjust_hsnow, attenuation_coef_snow
from beer_lambert_rt.constants import k_dry_snow, k_wet_snow, k_thin_snow


def test_adjust_hsnow_thin_wet_snow():
    hsnow = 0.02
    surface_temperature = 1.
    expected = hsnow
    target = adjust_hsnow(hsnow, surface_temperature)
    assert expected == target


def test_adjust_hsnow_thick_wet_snow():
    hsnow = 0.2
    surface_temperature = 1.
    expected = 0.17  # Assumes hssl_wet_snow is 0.03
    target = adjust_hsnow(hsnow, surface_temperature)
    assert expected == target


def test_adjust_hsnow_thin_dry_snow():
    hsnow = 0.02
    surface_temperature = -10.
    expected = hsnow
    target = adjust_hsnow(hsnow, surface_temperature)
    assert expected == target
    

def test_adjust_hsnow_thick_dry_snow():
    hsnow = 0.2
    surface_temperature = -10.
    expected = hsnow
    target = adjust_hsnow(hsnow, surface_temperature)
    assert expected == target


def test_attenuation_coef_snow_dry_snow():
    hsnow = 0.2
    surface_temperature = -10.
    expected = k_dry_snow
    target = attenuation_coef_snow(hsnow, surface_temperature)
    assert expected == target


def test_attenuation_coef_snow_thick_wet_snow():
    hsnow = 0.2
    surface_temperature = 1.
    expected = k_wet_snow
    target = attenuation_coef_snow(hsnow, surface_temperature)
    assert expected == target


def test_attenuation_coef_snow_thin_wet_snow():
    hsnow = 0.02
    surface_temperature = 1.
    expected = k_thin_snow
    target = attenuation_coef_snow(hsnow, surface_temperature)
    assert expected == target


# Add tests for snow transmittance
