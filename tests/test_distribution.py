"""Tests for snow and ice thickness distributions"""
import numpy as np

from beer_lambert_rt.distributions import (snow_depth_distribution,
                                           ice_thickness_distribution,
                                           snow_ice_distribution)


def test_snow_depth_distribution():
    """Tests that snow depth distribution returns probabilities
    sum to 1. within tolerance.
    """
    mean_snow_depth = 0.3
    nbins = 7
    factor = 3.
    center, prob = snow_depth_distribution(mean_snow_depth,
                                           nbins=nbins,
                                           factor=factor)
    assert np.allclose(prob.sum(), 1)


def test_ice_thickness_distribution():
    """Tests that snow depth distribution returns probabilities
    that sum to 1. within tolerance.
    """
    mean_ice_thickness = 1.5
    nbins = 15
    factor = 3.
    center, prob = ice_thickness_distribution(mean_ice_thickness,
                                              nbins=nbins,
                                              factor=factor)
    assert np.allclose(prob.sum(), 1.)


def test_snow_ice_distribution():
    """Tests that joint snow and ice thickness distribution
    sums to 1. within tolerance.
    """
    mean_snow_depth = 0.3
    nbins_snow = 7
    factor_snow = 3.
    mean_ice_thickness = 1.5
    nbins_ice = 15
    factor_ice = 3.
    snow_d, ice_d, prob = snow_ice_distribution(mean_ice_thickness, mean_snow_depth,
                                                nbins_snow=nbins_snow,
                                                max_factor_snow=factor_snow,
                                                nbins_ice=nbins_ice,
                                                max_factor_ice=factor_ice)
    assert np.allclose(prob.sum(), 1.)
