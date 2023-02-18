# Notes for refactoring code

Dependencies
 - xarray
 - scipy for distributions
 - matplotlib
 - cartopy
 
Extract data to separate modules
 - Robbies stats
 - AOPs

Move plotting, io and model to separate modules

Document processing chain

**Regridding data -> regrid and write data to files**
**Write month netcdf with SIC, SIT, snow depth, albedo, temp and Fsw0**

## Main model process

Loop through years in year_list
  Loop through months in month_list

    Calculate indices_year_month: - only use timesteps for years and months of interest
    
    Generate an output filename for PAR

    Open SIT file for year - is this monthly

    At line 457 - what is indices_year_month?

    For each day in month
        Load sea ice concentration  NSIDC regridded to 25 km
        Load sea ice thickness  
        Load snow depth  Glen's now depth
        Load albedo  APPx

        Calculate snow depth distribution for grid cell - currently 7 (I think)
          snow_depth_dist = snow_depth
          snow_dist_factor = (np.arange(1,n_snow_bins)*2 - 1.)/n_snow_bins - Mallet
          snow_depth_dist = h_s * snow_dist_factor

        Calculate ice thickness distribution for grid cell
          ice_thickness_distribution is calculated in lines 289 to 292
          follows similar approach to snow depth distribution but with a cutoff

        Foreach ice thickness and snow depth bin (7x15)
                Calculate transmittance for surface type lines 377 to 413
                Also see Eq 2, 3, and 4 in paper
                
        Transmittance for water is 1 - albedo_water, where albedo_water = 0.7
        However, in line 518 T_ow is set to 1 - alb from APPx

        Calculate weighted average transmissivity        