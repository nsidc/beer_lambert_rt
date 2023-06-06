"""Main model function and helper functions"""

from beer_lambert_rt.transmission import calculate_transmittance, transmission_open_water
from beer_lambert_rt.distribution import joint_transmission_distribution


def run_model(ice_thickness -> float,
              snow_depth -> float,
              albedo -> float,
              sw_radiation -> float,
              skin_temperature -> float,
              sea_ice_concentration -> float,
              pond_depth=0.,
              pond_fraction=None.,
              use_distribution=True,
              nsnow_class=7.
              max_snow_factor=3.,
              nice_class=15.,
              max_ice_factor=3.):
    """Runs Beer-Lambert RT model

    Arguments
    ---------
    :ice_thickness: (float) ice thickness in meters (scalar or array-like)
    :snow_depth: (float) snow depth in meters (scalar or array-like)
    :albedo: surface albedo [0-1] (scalar or array-like)
    :sw_radiation: Shortwave radiation (scalar or array-like)
    :skin_temperature: Skin temperature in degrees C (scalar or array-like)

    Keywords
    --------
    :sea_ice_concentration: Sea ice concentration [0-1] (scalar or array-like).  Default
                            is 1.
    :pond_depth: pond_depth in meters (scalar or array-like). Ignored if None.
    :pond_fraction: pond_fraction [0-1] (scalar or array-like). Only used if pond-depth
                    is not None. 
    :use_distribution: (boolean) Use ice_thickness and snow_depth to define snow and 
                       ice distribution. Default=True,
    :nsnow_class: Number of snow classes in snow depth distribution (scalar) Default=7.
    :max_snow_factor: Set maximum snow depth in distribution as max_snow_factor*snow_depth
                      Default=3.,
    :nice_class: **Not Used** Number of ice classes in ice thickness distribution (scalar) 
                 Default=15.
    :max_ice_factor: **Not Used** Set maximum ice thickness as max_ice_factor*ice_thickness
                     Default=3.

    :returns: TBD but PAR, Flux, ????
    """

    # Flatten arrays or do we need to do this



def get_mean_transmittance(ice_thickness,
                           snow_depth,
                           pond_depth,
                           surface_temperature,
                           use_distribution=True,
                           nbins_snow=7.
                           max_factor_snow=3.,
                           nbins_ice=15.,
                           max_factor_ice=3.):
    """Returns mean transmittance for a ice_thickness, snow_depth and pond_depth

    Need to add a pond transmittance with pond_fraction"""
    if use_distribution:
        hice_arr, hsnow_arr = joint_transmission_distribution(ice_thickness, snow_depth,
                                                              nbins_snow, max_factor_snow,
                                                              nbins_ice, max_factor_ice)
        hpond_arr = np.full_like(hice_arr, pond_depth)
        tsurf_arr = np.full_like(hice_arr, surface_temperature)
        transmittance = calculate_transmittance(hice_arr, hsnow_arr, hpond_arr, tsurf_arr)
    else:
        transmittance = calculate_transmittance(ice_thickness, snow_depth, pond_depth,
                                                surface_temperature)
    return transmittance
    
    
def calculate_flux_and_par(
        ice_thickness -> float,
        snow_depth -> float,
        albedo -> float,
        sw_radiation -> float,
        skin_temperature -> float,
        sea_ice_concentration -> float,
        pond_depth=0.,
        pond_fraction=None.,
        use_distribution=True,
        nsnow_class=7.
        max_snow_factor=3.,
        nice_class=15.,
        max_ice_factor=3.):
    """Calculates flux and PAR for one input.  Function can be mapped to scalar, 1D and 2D arrays"""
    # Calculate transmittance for ice fraction as distribution of single values
    ice_cover_transmittance = get_mean_transmittance(ice_thickness, snow_depth,
                                                     pond_depth, surface_temperature,
                                                     use_distribution=use_distribution)

    # Calculate flux for open water
    # ow_transmittance = (1 - albedo)  # Is this correct?
    
    # Calculate flux for ice covered portion
    # ice_transmittance = (1 - albedo) * mean_grid_transmittance

    # Calculate total flux
    # ice_swflux = surface_flux * ice_transmittance
    # ow_swflux = surface_flux * ow_transmittance

    # ice_par = ice_swflux * underice_flux2par
    # ow_par = ow_swflux * openwater_flux2par

    # total_par = (ice_par * sic) +
    #             (ow_par * (1 - sic))

    # Calculate mean flux
    
