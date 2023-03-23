"""Contains Juliennes original functions"""
import numpy as np

def get_f_att_snow(hsnow,hice,temperature):
# surface transmission layer thickness (m)
#surface transmission parameter
    # i_0_snw  =  0.45     # for wet snow (changed from 0.3)
    i_0_snw = 1.0       #for dry snow (changed from 0.3)
    i_0_ice = 0.26     # for ice  (may change)  Changed to 0.26 from 0.3

# surface transmission layer thickness (m)
    h_0_snw = 0.0     # for dry snow only
    h_0_ice = 0.1    # for bare ice ice  (may change !)
    K_i = 1
    K_s = 7.               #for dry snow

    if (temperature > 0):  #wet snow case
        K_s = 5.  #wet snow       #new coefficient for wet snow (used to be 7)
        i_0_snw = 0.45
        h_0_snw = 0.03;     # for wet snow only
        if (hsnow > 0.) & (hsnow <= 0.03):  #correction for SSL < 0.03
            K_s = 40.

#normal transmittance equation regardless of wet or dry snow
 #normal extinction for SSL > 0.03
    f_att_snow  = i_0_snw * np.exp(-K_s*(hsnow)) * np.exp(-K_i*hice)

#modify if the snow depth is 0cm
    if (hsnow == 0):
        if (hice < 0.5):
           f_att_snow = np.exp(-K_i*hice)
        elif (hice < 0.1):
            K_i=12
            f_att_snow= np.exp(-K_i*hice)
        elif (hice >=0.5) & (hice <=0.8):
            hssl = (1./3.) * hice - (1./6.)
            f_att_snow = i_0_ice * np.exp(-K_i*(hice-hssl))
        else:
            f_att_snow = i_0_ice * np.exp(-K_i*(hice-h_0_ice))

    return(f_att_snow)
