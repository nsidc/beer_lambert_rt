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


### Pseudo code for beer_lambert_rt lines 435 to 565

#### Variables

:fn: - output file name
:f_SIT, f, : - sea ice thickness file, ice concentration file

:f_bi: ice concentration [0-1]
:hi15: ice thickness distribution [nx, ny, nbin] nbin=15 - code is in l289 to 293
:h_s: snow depth input grid
:ds7: snow depth distribution [nx*ny, nbin]

:alb: - albedo from APPX
:temp: - skin temperature from APPX - Kelvin
:Fsw0: - short wave flux at surface from APPX

underice_flux2par = 3.5   - from Eq 10
openwater_flux2par = 2.3  - from Eq 9 Stroeve et al

Total flux is:

ice_transmittance = (1 - albedo) * mean_grid_transmittance
ow_transmittance = (1 - albedo)

surface_swflux * [(ice_transmittance * sic * underice_flux2par) +
                  (ow_transmittance * (1 - sic) * openwater_flux2par)]


Robbies data https://github.com/robbiemallett/light_sub_km/blob/main/use_quantiles.ipynb