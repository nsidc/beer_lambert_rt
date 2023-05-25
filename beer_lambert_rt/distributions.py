"""Functions to define ice thickness and snow depth distributions"""

import numpy as np
from scipy.stats import skewnorm


def ice_thickness_distribution(ice_thickness, nclass=15):
    """Returns an ice thickness distribution for a mean ice thickness.
    
    The distribution is based on the ITD used in Castro Morales et al 2015.
    
    A ITD is defined for the interval 0 to 3 * hi.  nclass ice thickness
    bins of equal width are defined and returned with the PDF of the distribution.
    
    Arguments
    ---------
    :hi: mean ice thickness
    :nclass: number of classes
    
    Returns
    -------
    tuple (bins, pdf)
    """
    max_hice_factor = 3.
    bin_width = max_hice_factor / nclass
    bins = np.arange(bin_width/2., max_hice_factor, bin_width) * ice_thickness
    pdf = np.array([0.0646, 0.1415, 0.173, 0.1272, 0.1114, 0.0824, 0.0665,
                     0.0541, 0.0429, 0.0347, 0.0287, 0.024, 0.0194, 0.016, 0.0136])
    return (bins, pdf)


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


def snow_depth_anomaly_distribution():
    """Returns skewnorm distribution for snow depth anomalies from
    Mallet et al (2021).
    
    :returns: scipy rv_continuous class for skewnorm dist
    """
    skewness = 2.54
    location = -1.11
    scale = 1.5
    rv = skewnorm(skewness, location, scale)
    return rv


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


def snow_depth_distribution(snow_depth, nbins=7, factor = 3):
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
    
    edge, width = get_bins(snow_depth_mean, nbins=nbins, factor=factor)
    std_edge = standardize_snow_depth(edge, snow_depth_mean)

    prob = snow_depth_anomaly_distribution().cdf(std_edge)
    fraction = np.diff(prob)
    fraction = fraction/fraction.sum()  # normailize to 1
    
    center = (edge[1:] + edge[:-1]) / 2.
    
    return center, fraction
