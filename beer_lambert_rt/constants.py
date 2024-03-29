"""Defines Apparent Optical Properties and other constants"""
import numpy as np


albedo_open_water = 0.07  # Albedo of open water

# Surface scattering layer thickness
hssl_ice = 0.1        # Ice
hssl_dry_snow = 0.0   # Dry snow has no SSL
hssl_wet_snow = 0.03  # Wet snow
hssl_thin_wet_snow = 0.0  # Thin wet snow

# Attenuation coefficients - prefixed with k
k_ice = 1.0        # Ice
k_thin_ice = 12.0  # Thin ice
k_dry_snow = 7.    # Dry snow
k_wet_snow = 5.    # Wet snow
k_thin_wet_snow = 40.  # Applied for hsnow > 0. and hsnow <= hssl_wet_snow

# Surface transmission parameters
i0_ice = 0.26       # Ice
i0_dry_snow = 1.0   # Dry snow
i0_wet_snow = 0.45  # Wet snow
i0_melt_ponds = 0.56  # Melt ponds

# Ice thickness classes
gice_pdf = np.array([0.0646, 0.1415, 0.173,
                     0.1272, 0.1114, 0.0824,
                     0.0665, 0.0541, 0.0429,
                     0.0347, 0.0287, 0.024,
                     0.0194, 0.016, 0.0136])
nbins_ice = len(gice_pdf)
max_factor_ice = 3.

# Snow distribution bins
nbins_snow = 7
max_factor_snow = 3.

# Conversion factors for SW flux to PAR
underice_flux2par = 3.5   # from Eq 10
openwater_flux2par = 2.3  # from Eq 9 Stroeve et al

# Add snow distribution to constants
