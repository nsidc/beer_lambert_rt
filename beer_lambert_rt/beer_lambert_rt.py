#!/usr/bin/env python2

# -*- coding: utf-8 -*-

"""

Created on Wed Mar 24 11:43:27 2021



@author: stroeve

"""
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,'/anaconda2/pkgs')
import numpy as np
from scipy.stats import skewnorm, kstest
from numpy import *
import netCDF4
from netCDF4 import Dataset
import os
import datetime
import glob
import os
import xarray as xr
#import matplotlib
#matplotlib.use('Agg')
#import ffgrid2
# from pylab import *
# from PIL import Image
# from mpl_toolkits.basemap import Basemap
#from mpl_toolkits.basemap import shiftgrid, cm
#from mpl_toolkits.basemap import shiftgrid, cm
#from pyhdf.SD import SD
#import carte_s
#from xlrd import xldate
#from osgeo import gdal
#from sklearn.metrics import mean_square_error
# from scipy.interpolate import griddata
# import pyproj as proj
#from osgeo import gdal_array
#from osgeo import osr
# import pandas as pd
# import xarray as xr
from scipy.interpolate import griddata
import pyproj as proj
import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
import tqdm
import cartopy
import cartopy.crs as ccrs

args = proj.Proj(proj="aeqd", lat_0=90, lon_0=0, datum="WGS84", units="m")

crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic

#%% LOAD Function
def regrid(data_in,
           lon_in,
           lat_in,
           lon_out,
           lat_out,
           method='nearest'):

    xout, yout = proj.transform(crs_wgs, args, np.array(lon_out),np.array(lat_out))

    xin, yin = proj.transform(crs_wgs, args, np.array(lon_in),np.array(lat_in))

    output = griddata((xin.ravel(),yin.ravel()),
                    np.array(data_in).ravel(),
                    (xout,yout),
                    method=method)
   
    return(output)

#%% LOAD Function
def regrid_fast(data_in,
           lon_in,
           lat_in,
           lon_out,
           lat_out,
           fill_val=np.nan):

    xout, yout = proj.transform(crs_wgs, args, np.array(lon_out),np.array(lat_out))

    xin, yin = proj.transform(crs_wgs, args, np.array(lon_in),np.array(lat_in))

    points = np.column_stack((xin.ravel(),yin.ravel()))
    tri = Delaunay(points)  # Compute the triangulation

    output = np.full((data_in.shape[0],xout.shape[0],xout.shape[1]),fill_val)   
   
    for i in tqdm.trange(0,data_in.shape[0]):

        interpolator = LinearNDInterpolator(tri, data_in[i].ravel())

        output[i] = interpolator((xout,yout))
   
    return(output)

#%% LOAD Function
#function to plot the data given the data and lat/lons
def plot(data,latsy,lonsx,string):
    # Modules
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    maxv=data.max()
    print('maximum data value ',data.max())
    if string == 'sic':
        label_unit='SIC (%)'
        minv=0.
        maxv=100.
        # if maxv<=1.:
        #     data=data*100.
        data=data*100.
    elif string == 'sit':
        label_unit='Sea Ice Thickness (m)'
        # data=data/100.
        minv=0.0
        maxv=2.0
    elif string == 'snow':
        data=data*100.
        label_unit='Snow Depth (cm)'
        minv=0.0
        maxv=20.0  
    elif string == 'alb':
        label_unit='Albedo'
        minv=0.0
        maxv=100.0
    elif string == 'par':
        label_unit='PAR'
        minv=0.0
        maxv=5
       
#switch to using cartopy for plotting
#for Hudson Bay set the latitude to range from 55 to 70N and 50 to 100W
   
# Parameters
    prjplot = ccrs.NorthPolarStereo(central_longitude=-80,true_scale_latitude=70) # Warning: This is almost certainly different from the data's projection
    fig=plt.figure(figsize=(6.5,6.5))
    ax=plt.axes(projection=ccrs.NorthPolarStereo())
    ax.set_extent([-180,180,90,50],ccrs.PlateCarree())
    # ax.set_extent([-110,-60,70,50],ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.LAND, edgecolor='black',zorder=1)
    ax.set_title(string)
   
   
    bg=ax.pcolormesh(lonsx,latsy,data,vmin=minv,vmax=maxv,transform=ccrs.PlateCarree(),cmap='plasma')
    cb=fig.colorbar(bg,orientation='vertical',shrink=1)
    cb.set_label(label_unit,fontsize='x-large')
   
#%% LOAD Function
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

year_list=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
month_list=[1,2,3,4,5,6]
month_L_list=['JAN','FEB','MAR','APR','MAY','JUN']


#get time for the snow depth data - creates a array starting in August 1 1980
nc = netCDF4.Dataset ('/Volumes/LaCie/under-ice-light/snow_depth/SM_snod_ERA5_01Aug1980-31Jul2021_v01.nc')
time=nc.variables['time'][:]
time_convert = netCDF4.num2date(time[:], nc.variables['time'].units)
nc.close()
#Robbie's statistics

statistics = {'a': 2.542562886886376,
  'loc': -1.114525560819975,
  'scale': 1.4973819434202296,
  'CV': 0.41696167189340216}

#initialize array to fill
Under_ice_PAR=np.zeros((31,361,361))


#%% LOAD Function
def get_latlon():
#get lat/lons
    file_APPX='/Volumes/LaCie/under-ice-light/APPX/1988/Polar-APP-X_v02r00_Nhem_1400_d19880401_c20190624.nc'
    nc = netCDF4.Dataset (file_APPX)
    latX=nc.variables['latitude'][:,:]
    lonX=nc.variables['longitude'][:,:]
    return latX,lonX

#%% LOAD Function
def create_outputdata(fn,indices_year_month,varid):
    ncfile = Dataset(fn, 'w', format='NETCDF4')
    time = ncfile.createDimension('time', None)
    x = ncfile.createDimension('x', 361)
    y = ncfile.createDimension('y', 361)

    times=ncfile.createVariable("time","f4",("time",))
    times.units='days'
    times.long_name='time'
    lats = ncfile.createVariable("lat", "f4", ('x','y',))
    lats.units='degrees_north'
    lats.long_name='latitude'
    lons = ncfile.createVariable("lon", "f4", ('x','y',))
    lons.units='degrees_ease'
    lons.long_name='longitude'

    if (varid == 'PAR'):
        value = ncfile.createVariable('PAR', 'f4', ('time','x', 'y'))
        value.units = 'W m-2'
    if (varid == 'bloom'):
        value = ncfile.createVariable('Bloom Onset', 'f4', ('time','x', 'y'))
        value.units = 'day of year'
    result=get_latlon()
    lats[:,:]=result[0]
    lons[:,:]=result[1]
    times[:]=np.arange(1,len(indices_year_month))
    return ncfile,value,lats,lons

#%% LOAD Function
def get_SIC(fn_SIC):
    SIC=np.zeros([361,361])
    A = np.fromfile(fn_SIC, dtype='uint16')
    c=-1
    for i in range (0,361):
        for j in range (0,361):
            c=c+1
            SIC[i,j] = A[c]               
    SIC_2=flipud(SIC)
    # plot(SIC,lats,lons,'sic')
    plt.figure(0)
    plt.imshow(SIC/100.)
    plt.title('SIC')
    plt.show()
    f_bi=SIC/100.
    f_bi=reshape(f_bi,361*361)
    return(f_bi)   

#%% LOAD Function
def get_SIT(fn_SIT,year,month,zz):  #gets the SIT data and computes the thickness distribution per grid cell
   
    nc = netCDF4.Dataset(fn_SIT)
    # DOY=nc.variables['DOY'][:]
    # year_start=where(DOY==1)
  
    DOY=nc.variables['Day'][:]  #for these files it starts on 1 October and thus Jan 1 equals 92
    year_start=where(DOY==92)
    year_DOY_count=np.asarray(DOY[year_start[0][0]:])  #gives you all the indices starting from 92 onwards (i.e. Jan 1 onwards)
    print('inside get_SIT to check values ')
    print('year and month being processed',year,month)
    # print(year_DOY_count)
    # print('length to loop over',len(year_DOY_count))
    # date_seaice=[]
    delta=datetime.datetime(year,month,1)-datetime.datetime(year,1,1)
    # print('delta ',delta)
    delta=delta.days+zz
    print('deltas ',delta)

    lons_ease2=nc.variables['Longitude']
    lats_ease2=nc.variables['Latitude']
        

    # for kk in range (0, len(year_DOY_count)):
    #     date_seaice.append(datetime.datetime(year, 1, 1) + datetime.timedelta(year_DOY_count[kk] - 1))
    #     indices_seaice = [i for i, x in enumerate(date_seaice) if x.month== month]
    #     # print('indices ',indices)
    # print(indices_seaice)

    # th_ice=nc.variables['Sea_Ice_Thickness'][year_start[0][0]+indices_seaice[zz],:,:] #premier indice, donner le temps pour mars et pour avril [11169:11199]# ->march 2011    [11200:11229] -> April 2011
    print('index for the DOY for the SIT ',year_start[0][0]+delta)

    th_ice=nc.variables['Sea Ice Thickness'][year_start[0][0]+delta,:,:] #delta is based on difference between January 1 and the month that is inserted
    plt.figure(4)
    plt.imshow(th_ice)
    plt.title('original SIT')
    th_ice_ease=regrid(th_ice,lons_ease2,lats_ease2,lons,lats)
    # plt.figure(5)
    # plt.imshow(th_ice_ease)
    # plt.title('ease gridded')
    # hi=flipud(th_ice_ease) #flip to rightside up

    # plot(th_ice_ease,lats,lons,'sit')
    plt.figure(1)
    plt.imshow(th_ice_ease)
    plt.title('SIT')
    plt.show()
    hi=reshape(th_ice_ease,361*361)
    h_cutoff=3.
    hi15=np.zeros([361*361,15])

    for i in range (1,16):
        factor2=(2*i - 1)/15.
        hi15[:,i-1]=hi*factor2    
        hi15[:,i-1]=(h_cutoff/2.)*hi15[:,i-1]
    return(hi15)

#%% LOAD Function
def get_std_from_mean(mean_depth, CV):
    std = mean_depth * CV
   
    return (std)

#%% LOAD Function
def depth_distribution_from_mean_depth_and_edges(mean_depth, dep_bin_edges, statistics):
    dep_bin_centres = dep_bin_edges[:-1] + (dep_bin_edges[1] - dep_bin_edges[0]) / 2
    std = get_std_from_mean(mean_depth, statistics['CV'])
    std_bin_edges = (dep_bin_edges - mean_depth) / std
    std_bin_centres = std_bin_edges[:-1] + (std_bin_edges[1] - std_bin_edges[0]) / 2
    std_bw = np.nanmean(np.diff(std_bin_edges))
    fit = skewnorm.pdf(std_bin_centres,
                       statistics['a'],
                       statistics['loc'],
                       statistics['scale']) * std_bw
   
    return (dep_bin_centres, fit)


#%% LOAD Function
def make_depth_dist(mean_depth, n_bins = 10, max_depth = 1.0):
   
    bin_edges = np.linspace(0,max_depth,n_bins+1)
    bin_width = np.diff(bin_edges)[0]
    bin_centres, probabilities = depth_distribution_from_mean_depth_and_edges(mean_depth,bin_edges,statistics)
   
    return (bin_centres, probabilities)

#%% LOAD Function
def get_SND(fn_SND,indices_year_month,zz): #gets the snow depth and computes the snow depth distribution per grid cell

    h_s=np.zeros([361,361])
    nc = netCDF4.Dataset(fn_SND)
    snod=nc.variables['snod'][indices_year_month[0]+zz,:,:] #premier indice, donner le temps pour mars et pour avril [11169:11199]# ->march 2011    [11200:11229] -> April 2011
    # plot(snod,lats,lons,'snow')
    h_s=flipud(snod)     #h_s=flipud(snod)  
    plt.figure(3)
    plt.imshow(h_s)
    plt.title('snow depth')
    plt.show()
    h_s=reshape(h_s,361*361)

    return h_s

#%% LOAD Function
def get_alb_SW(fn_APPX): #returns both the albedo, temperature and incoming solar radiation

    nc= netCDF4.Dataset(fn_APPX)
    alb=nc.variables['cdr_surface_albedo'][:,:]
    ind=where(alb>1000)
    alb[ind]=float(nan)
    alb=alb[0]
    # plot(alb,lats,lons,'alb')
    plt.figure(2)
    plt.imshow(alb)
    plt.title('albedo')
    plt.show()

    # alb=flipud(alb)
    alb=reshape(alb,361*361)

    down=nc.variables['cdr_surface_downwelling_shortwave_flux'][:,:]
    ind=where(down>1000)
    down[ind]=float(nan)
    Fsw0=down[0]
    # Fsw0=flipud(Fsw0)
    Fsw0=reshape(Fsw0,361*361)

    data=nc.variables['cdr_surface_temperature'][:,:]
    ind=where(data>1000)
    data[ind]=float(nan)
    temp=data[0]
    # temp=flipud(temp)
    temp=reshape(temp,361*361)

    return alb, temp, Fsw0



#%% LOAD Function
def get_f_att_snow(hsnow,hice,temperature):
# surface transmission layer thickness (m)
#surface transmission parameter
    # i_0_snw  =  0.45     # for wet snow (changed from 0.3)
    i_0_snw = 1.0       #for dry snow (changed from 0.3)
    i_0_ice   =  0.26     # for ice  (may change)  Changed to 0.26 from 0.3

# surface transmission layer thickness (m)
    h_0_snw  =  0.0     # for dry snow only
    h_0_ice   =  0.1    # for bare ice ice  (may change !)
    K_i  = 1
    K_s=7.               #for dry snow

    if (temperature > 0):  #wet snow case
        K_s=5.  #wet snow       #new coefficient for wet snow (used to be 7)
        i_0_snw = 0.45
        h_0_snw  =  0.03;     # for wet snow only
        if (hsnow > 0.) & (hsnow <= 0.03):  #correction for SSL < 0.03
            K_s=40.

#normal transmittance equation regardless of wet or dry snow
    f_att_snow  = i_0_snw*exp(-K_s*(hsnow))* exp(-K_i*hice) #normal extinction for SSL > 0.03

#modify if the snow depth is 0cm
    if (hsnow == 0):
        if (hice < 0.5):
           f_att_snow=exp(-K_i*hice)
        elif (hice < 0.1):
            K_i=12
            f_att_snow=exp(-K_i*hice)
        elif (hice >=0.5) & (hice <=0.8):
            hssl=(1./3.)*hice-(1./6.)
            f_att_snow=i_0_ice*exp(-K_i*(hice-hssl))
        else:
            f_att_snow=i_0_ice*exp(-K_i*(hice-h_0_ice))

    return(f_att_snow)


# #surface transmission parameter
# i_0_snw  =  0.3;     # for snow
# i_0_ice   =  0.3;     # for ice  (may change)
# # surface transmission layer thickness (m)
# h_0_snw  =  0.03;     # for snow
# h_0_ice   =  0.1;    # for bare ice ice  (may change !)
# K_i  = 1;

hpdf = [0.0646, 0.1415, 0.173, 0.1272, 0.1114, 0.0824, 0.0665, \
                    0.0541, 0.0429, 0.0347, 0.0287, 0.024,0.0194, 0.016, 0.0136]
hpdf=np.asarray(hpdf)

n_i, n_j=361,361 #initialize the lat/lon indices


dir='/Volumes/LaCie/under-ice-light/'
f_SND = dir+'/snow_depth/SM_snod_ERA5_01Aug1980-31Jul2021_v01.nc'


#note in the subroutines I'm returning arrays that are 361*361
for ii in range(0,3):
    for jj in range(0,4):
# for ii in range(0,len(year_list)):
    # for jj in range(,len(month_list)):
        #this section is about building the output file name based on SIT input data
        #the indices are to help find the right snow data to use
        indices_year_month = [i for i, x in enumerate(time_convert) if x.year == year_list[ii] and x.month== month_list[jj]]
        # print('indices_year_month ',indices_year_month)     

        #create outputfilename and dataframe and information that will go into it
        fn ='/Users/stroeve/Documents/Ecolight/daily/daily_under-ice_PAR_{value}_{value2}_CPOM.nc'.format(value=str(year_list[ii]),value2=str(month_L_list[jj]))
        # fn =dir+'/daily/daily_under-ice_PAR_{value}_{value2}_CPOM.nc'.format(value=str(year_list[ii]),value2=str(month_L_list[jj]))
        print('opening output filename ',fn)
        ncfile, value, lats, lons=create_outputdata(fn,indices_year_month,'PAR')

         # f_SIT ='/Volumes/LaCie/under-ice-light/SIT/cryosat2_cpomOIrfb_seaicethickness_nh_daily_25km_{value2}-{value}_v1.nc'.format(value=str(year_list[ii]),value2=str(year_list[ii]-1)); # Or sys.argv[1]
        f_SIT=dir+'SIT/SIT_CS2_CPOM_{value2}-{value}.nc'.format(value=str(year_list[ii]),value2=str(year_list[ii]-1))
        print('opening SIT file ',f_SIT)
        print('')

   
#get all the input files for the various input fields for each day in the month      
        for zz in range(0,len(indices_year_month)):
            f = open('/Volumes/LaCie/under-ice-light/SIC/{value}/nt_{value1}{value2}{value3}_f17_v01_n.binEASE.bin'.format(value=str(year_list[ii]),value1=str(year_list[ii]),value2=str(month_list[jj]).zfill(2),value3=str(zz+1).zfill(2)), 'rb');
            f_bi=get_SIC(f)
            print('')
            print('opening SIC file ',f)
            print('')

            # # f_SIT ='/Volumes/LaCie/under-ice-light/SIT/cryosat2_cpomOIrfb_seaicethickness_nh_daily_25km_{value2}-{value}_v1.nc'.format(value=str(year_list[ii]),value2=str(year_list[ii]-1)); # Or sys.argv[1]
            # f_SIT=dir+'SIT/SIT_CS2_CPOM_{value2}-{value}.nc'.format(value=str(year_list[ii]),value2=str(year_list[ii]-1))
            hi15=get_SIT(f_SIT,year_list[ii],month_list[jj],zz)
            print('done reading SIT for month and day of month',month_list[jj],zz+1)
            print('')

           #get the snow depth field corresponding to the correct indices in SM files
            h_s = get_SND(f_SND,indices_year_month,zz)
            print('done getting snow depth for day of month ',zz+1)

            # listdir=listdir_nohidden('/Volumes/LaCie/under-ice-light/APPX/{value}/{value2}/'.format(value=str(year_list[ii]),value2=month_L_list[jj]));

            listdir=listdir_nohidden('/Volumes/LaCie/under-ice-light/APPX/{value}'.format(value=str(year_list[ii])));
            data_dir = sort(listdir);#,value6=weird2)_c{value6} # Or sys.argv[1]
            delta=datetime.datetime(year_list[ii],month_list[jj],1)-datetime.datetime(year_list[ii],1,1)
            f_APPX=data_dir[delta.days+zz]         
            print('opening APPX file ',data_dir[delta.days+zz])
            alb, temp, Fsw0 = get_alb_SW(f_APPX)
            temp=temp-273.16
         

#initialize empty arrays for the tranmisttance
            hssl=np.zeros((361*361,15),dtype=float32)  
            T_ow=np.zeros(361*361,dtype=float32)
            T_snow=np.zeros(361*361,dtype=float32)
            Fsw_tr_new=np.zeros((361*361,15),dtype=float32)
            # hs7=np.zeros((361*361,10),dtype=float32)
            # hs7_prob=np.zeros((361*361,10),dtype=float32)
# initialisation snow attenuation coeff
            K_s=np.zeros([361*361,10])       

# initialisation intermediate steps
            f_att_snow=np.zeros((361*361,10,15),dtype=float32)
            i_s_hom=np.zeros((361*361,15),dtype=float32)
            t_s_hom=np.zeros((361*361,15),dtype=float32)

# hs array between 0 and 2 times mean snow depth
            hs7=np.zeros((361*361,7)) ## ice thickness distribution
            for i in range (1,8):
                factor_hs=(2*i - 1)/7.    ## factor for distribution
                hs7[:,i-1]=h_s*factor_hs 
            #redo this using the fit by Robbie
            # for i in range(n_i*n_j):
            #     #get the snow depth in the grid cell
            #     snowdepth=h_s[i].data
            #     print('snowdepth ',snowdepth)
            #     #call the distribution function
            #     bin_centres, probabilities = make_depth_dist(snowdepth,n_bins=10,max_depth=2*snowdepth)
            #     #save the snow depth bins and their probabilities
            #     hs7[i,:]=bin_centres
            #     hs7_prob[i,:]=probabilities

        ## transmittance open water
            T_ow[:] = (1 - alb[:]);  
            # exit()
           
      #loops on ITD and assign K_s according to wet/dry snow       
            print('processing for day of month ',zz)
            for ll in range(15):  #loop over the ice thickness distribution
                for kk in range(0,7):  #loop over snow depth distribution
                    for igrid in range(361*361): #loop over full grid
                        hsnow=hs7[igrid,kk]
                        hice=hi15[igrid,ll]
                        temperature=temp[igrid]
                        f_att_snow[igrid,kk,ll]=get_f_att_snow(hsnow,hice,temperature)

            index=where(f_att_snow>1)
            f_att_snow[index]=1

            #integrate over all snow depth transmissivities
            for igrid in range(361*361):
                for ll in range(15):
                    i_s_hom[igrid,ll] = sum((1./7.) * f_att_snow[igrid,:,ll]); # integrated transmission

            for ll in range(15):
                t_s_hom[:,ll] = ((1-alb[:]) * i_s_hom[:,ll])  ;
                Fsw_tr_new[:,ll] = Fsw0[:]* ((t_s_hom[:,ll] * f_bi[:]*3.51) + (T_ow[:] * (1-f_bi[:]))*2.30);

# sum ITD 15 classes and apply pdf
            t_s_hom_sum=np.zeros(361*361)
            Fsw_tr_new_sum=np.zeros(361*361)
            for i in range (0,361*361):
                t_s_hom_sum[i]=sum(t_s_hom[i,0:15]*hpdf[0:15])
                Fsw_tr_new_sum[i]=sum(Fsw_tr_new[i,0:15]*hpdf[0:15])
        #end loop for SIT classse
            sys.stdout.flush()   

# change shape to 2D array for map plotting
            T_snow=np.zeros([361,361])
            Fsw_TR_NEW=np.zeros([361,361])  #under-ice PAR
            c=-1
            for i in range (0,361):
                for ll in range (0,361):
                    c=c+1
                    T_snow[i,ll]=t_s_hom_sum[c]
                    Fsw_TR_NEW[i,ll]=Fsw_tr_new_sum[c]
           
        #file output file
            value[zz, :, :] = Fsw_TR_NEW
     
        ncfile.close(); print('Output file is closed')
