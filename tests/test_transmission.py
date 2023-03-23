import pytest

import beer_lambert_rt.transmission as transmission

from beer_lambert_rt.constants import (hssl_ice, hssl_dry_snow,
                                       hssl_wet_snow, hssl_thin_wet_snow,
                                       k_ice, k_thin_ice,
                                       k_dry_snow, k_wet_snow, k_thin_wet_snow,
                                       i0_ice, i0_dry_snow, i0_wet_snow, i0_melt_ponds,
                                       albedo_open_water)

SURFACE_CONDITION = {
    
    "dry_snow": {
        "hice": 1.5,
        "hsnow": 0.3,
        "hpond": 0.0,
        "skin_temperature": -10.0,
        "expected_hssl_snow": hssl_dry_snow,
        "expected_hssl_ice": 0.0,
        "expected_surface_transmission": i0_dry_snow,
    },
    
    "wet_snow": {
        "hice": 1.5,
        "hsnow": 0.3,
        "hpond": 0.0,
        "skin_temperature": 0.0,
        "expected_hssl_snow": hssl_wet_snow,
        "expected_hssl_ice": 0.0,
        "expected_surface_transmission": i0_wet_snow,
    },
    
    "thin_wet_snow": {
        "hice": 1.5,
        "hsnow": 0.01,
        "hpond": 0.0,
        "skin_temperature": 0.0,
        "expected_hssl_snow": hssl_thin_wet_snow,
        "expected_hssl_ice": 0.0,
        "expected_surface_transmission": i0_wet_snow,
    },
    
    "thick_bare_ice": {
        "hice": 1.5,
        "hsnow": 0.0,
        "hpond": 0.0,
        "skin_temperature": 0.0,
        "expected_hssl_snow": 0.0,
        "expected_hssl_ice": hssl_ice,
        "expected_surface_transmission": i0_ice,
    },
    
    "medium1_bare_ice": {
        "hice": 0.7,
        "hsnow": 0.0,
        "hpond": 0.0,
        "skin_temperature": 0.0,
        "expected_hssl_snow": 0.0,
        "expected_hssl_ice": pytest.approx(0.06666667),
        "expected_surface_transmission": i0_ice,
    },
    
    "medium2_bare_ice": {
        "hice": 0.3,
        "hsnow": 0.0,
        "hpond": 0.0,
        "skin_temperature": 0.0,
        "expected_hssl_snow": 0.0,
        "expected_hssl_ice": 0.0,
        "expected_surface_transmission": i0_ice,
    },
    
    "thin_bare_ice": {
        "hice": 0.09,
        "hsnow": 0.0,
        "hpond": 0.0,
        "skin_temperature": 0.0,
        "expected_hssl_snow": 0.0,
        "expected_hssl_ice": 0.0,
        "expected_surface_transmission": i0_ice,
    },
    
    "melt_pond": {
        "hice": 1.5,
        "hsnow": 0.0,
        "hpond": 0.3,
        "skin_temperature": 0.0,
        "expected_hssl_snow": 0.0,
        "expected_hssl_ice": 0.0,
        "expected_surface_transmission": i0_melt_ponds,
    },
    
    }


@pytest.mark.parametrize(
    "stype",
    SURFACE_CONDITION.keys(),
)
def test_hssl_snow(stype):
    hsnow = SURFACE_CONDITION[stype]["hsnow"]
    skin_temperature = SURFACE_CONDITION[stype]["skin_temperature"]
    expected = SURFACE_CONDITION[stype]["expected_hssl_snow"]
    result = transmission.green_edge_hssl_snow(hsnow, skin_temperature)
    assert expected == result


@pytest.mark.parametrize(
    "stype",
    SURFACE_CONDITION.keys(),
)
def test_hssl_ice(stype):
    hsnow = SURFACE_CONDITION[stype]["hsnow"]
    hice = SURFACE_CONDITION[stype]["hice"]
    hpond = SURFACE_CONDITION[stype]["hpond"]
    expected = SURFACE_CONDITION[stype]["expected_hssl_ice"]
    result = transmission.green_edge_hssl_ice(hice, hsnow, hpond)
    assert expected == result


@pytest.mark.parametrize(
    "stype",
    SURFACE_CONDITION.keys(),
)
def test_surface_transmission(stype):
    hsnow = SURFACE_CONDITION[stype]["hsnow"]
    hice = SURFACE_CONDITION[stype]["hice"]
    hpond = SURFACE_CONDITION[stype]["hpond"]
    skin_temperature = SURFACE_CONDITION[stype]["skin_temperature"]
    expected = SURFACE_CONDITION[stype]["expected_surface_transmission"]
    result = transmission.select_surface_transmission(hice, hsnow, hpond, skin_temperature)
    assert expected == result


@pytest.mark.parametrize(
    "stype",
    SURFACE_CONDITION.keys(),
)
def test_attenuation_ice(stype):
    hice = SURFACE_CONDITION[stype]["hice"]
    expected = SURFACE_CONDITION[stype]["expected_attenuation"]
    result = transmission.select_attenuation_ice(hice)
    assert expected == result


# def test_green_edge_dry_snow():
#     """Tests green_edge_hssl_snow for dry snow"""
#     stype = "dry_snow"
#     check_hssl_snow(stype)
    
    
# def test_green_edge_wet_snow():
#     """Tests green_edge_hssl_snow for wet snow"""
#     stype = "wet_snow"
#     check_hssl_snow(stype)
    
    
# def test_green_edge_thin_wet_snow():
#     """Tests green_edge_hssl_snow for thin wet snow"""
#     stype = "thin_wet_snow"
#     check_hssl_snow(stype)
    

# def test_green_edge_snow_bare_ice():
#     pass


# def test_green_edge_ice_

# def test_green_edge_thick_bare_ice():
#     """Tests green_edge_hssl_snow for thin wet snow"""
#     stype = "thin_bare_ice"
#     check_hssl_ice(stype)
    
    
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
