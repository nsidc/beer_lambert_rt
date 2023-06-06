"""Functions to define ice thickness and snow depth distributions"""

import numpy as np
from scipy.stats import skewnorm


"""Returns skewnorm distribution for snow depth anomalies from
Mallet et al (2021).

:returns: scipy rv_continuous class for skewnorm dist
"""
skewness = 2.54
location = -1.11
scale = 1.5
snow_depth_anomaly_distribution = skewnorm(skewness, location, scale)


def ice_thickness_distribution(ice_thickness, nbins=15, factor=3.):
    """Returns an ice thickness distribution for a mean ice thickness.
    
    The distribution is based on the ITD used in Castro Morales et al 2015.
    
    A ITD is defined for the interval 0 to 3 * hi.  nclass ice thickness
    bins of equal width are defined and returned with the PDF of the distribution.
    
    Arguments
    ---------
    :hi: mean ice thickness
    :nbins: number of bins - fixed and does nothing
    :factor: maximum ice thickness factor - fixed and does nothing
    
    Returns
    -------
    tuple (bins, pdf)
    """
    prob = np.array([0.0646, 0.1415, 0.173, 0.1272, 0.1114,
                     0.0824, 0.0665, 0.0541, 0.0429, 0.0347,
                     0.0287, 0.024, 0.0194, 0.016, 0.0136])

    max_ice_factor = 3.
    nbins = 15
    edge, width = get_bins(ice_thickness, nbins=nbins, factor=max_ice_factor,
                           loc='center')
    return (edge, prob)


# Put these in script
def snow_depth_std(snow_depth_mean):
    """Returns standard deviation of snow depths"""
    cv = 0.417
    return cv * snow_depth_mean


def standardize_snow_depth(snow_depth, snow_depth_mean):
    """Returns standardized snow depths
    
    :snow_depth: snow depths in meters (array-like)
    :snow_depth_mean: mean snow depth (scalar)
    
    :returns: array of standardized snow depths
    """
    return (snow_depth - snow_depth_mean) / snow_depth_std(snow_depth_mean)


def get_bins(xmean, nbins=7, factor=2., loc=None):
    """Returns bin edges and bin widths for a thickness/depth distribution

    :xmean: mean thickness/depth (float)
    :nbins: number of bins in distribution (int)
    :factor: factor to set maximum thickness, where maximum thickness is
             factor*xmean (float)
    :loc: selects edge to return (string) if None returns all bin edges

    :returns: edges, width. (float array) If loc is None, array is nbins+1 edges from
              0 to factor*xmean.  If loc is "lower", "center" or "upper" returns
              nbin-size array where the lower edge, central value, or upper edge
              of each bin is returned.  width is array with nbins elements that contains
              the width of each bin.
    """
    edges = np.linspace(0., xmean*factor, nbins+1)
    width = np.diff(edges)
    if loc == "lower":
        return edges[:-1], width
    elif loc == "upper":
        return edges[1:], width
    elif loc == "center":
        return (edges[:-1] + edges[1:])/2., width
    return edges, width


def snow_depth_distribution(snow_depth, nbins=7, factor=3.):
    """Returns a discrete snow depth distribution
    
    :snow_depth: mean snow depth
    :nbins: number of bins in distribution
    :factor: factor to set maximum snow depth as function of mean snow depth
    
    :returns: bin center depth, fraction of dsitribution in bin
    
    The .cdf() method is used instead of .pdf because this returns the cumulative
    probability (fraction below a bin edge).  Differencing this using np.diff
    returns the fraction of the disrete distribution in each bin.
    
    NB. If the maximum snow depth (set by factor) is too small, so that not all of
    the continuous distribution is covered by the discrete distribution, the sum
    fractions returned by snow_depth_anomaly_distribution.cdf() will not sum to 1.
    To solve this fraction is normalized by the sum of fraction.
    """
    
    edge, width = get_bins(snow_depth, nbins=nbins, factor=factor)
    std_edge = standardize_snow_depth(edge, snow_depth)

    prob = snow_depth_anomaly_distribution.cdf(std_edge)
    fraction = np.diff(prob)
    fraction = fraction/fraction.sum()  # normailize to 1
    
    center = (edge[1:] + edge[:-1]) / 2.
    
    return center, fraction


def snow_ice_distribution(ice_thickness_mean, snow_depth_mean, 
                          nbins_ice=15, max_factor_ice=3.,
                          nbins_snow=7, max_factor_snow=3.):
    """Returns combined distributions of snow depth and ice thickness, 
    along with a joint probability (% fraction) of area

    Arguments
    ---------
    :ice_thickness_mean: mean ice thickness in meters
    :snow_depth_mean: mean snow depth in meters

    Keywords
    --------
    :nbins_ice: number of ice bins to use (default=15)
    :max_factor_ice: maximum ice thickness factor (default=3.)
    :nbins_snow: number of snow bins to use (default=7)
    :max_factor_snow: maximum ice thckness factor (default=3.)
    """
    snow_depth_dist, snow_prob = snow_depth_distribution(snow_depth_mean,
                                              nbins=nbins_snow,
                                              factor=max_factor_snow)
    ice_thickness_dist, ice_prob = ice_thickness_distribution(ice_thickness_mean,
                                                    nbins=nbins_ice,
                                                    factor=max_factor_ice)
    ice_thick_2d, snow_depth_2d = np.meshgrid(ice_thickness_dist,
                                              snow_depth_dist)
    joint_prob = np.outer(snow_prob, ice_prob)
    
    return ice_thick_2d.flatten(), snow_depth_2d.flatten(), joint_prob.flatten()
