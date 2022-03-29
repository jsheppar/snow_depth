import os
import shutil
import pandas as pd
import h5py
import numpy as np
import numpy.ma as ma
import xarray as xr
import rasterio
import rioxarray
import geoviews as gv
from holoviews import opts
from pyproj import Transformer
import matplotlib.pyplot as plt
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 

def make_dist_alongtrack(ph_count, seg_length, dist_ph):
    repeat_num = np.cumsum(seg_length) - seg_length[0]
    dist_alongtrack = np.repeat(repeat_num, ph_count)
    dist_alongtrack += dist_ph
    return dist_alongtrack

def coords_trans(lon, lat):
    # convert coords to UTM 10
    x = []
    y = []
    transformer = Transformer.from_crs(4326, 32610)
    points = list(zip(lat, lon))
    for pt in transformer.itransform(points):
        y.append(pt[0])
        x.append(pt[1])
    return (x, y)


def create_da(lon_ph, lat_ph, x, y, h_ph, q2, q3, q4, dist_alongtrack, filename, loc, rgt, beam):
    data_grouped = np.vstack((h_ph, lon_ph, lat_ph, x, y, q2, q3, q4))
    labels = ['h', 'lon', 'lat', 'x', 'y', 'q2', 'q3', 'q4']
    attrs = {'dataset': 'ATL03', 'granule': filename, 'location': 'Lake Louise, AK', 'RGT': rgt, 'Beam': beam}
    da = xr.DataArray(data_grouped, coords=[labels, dist_alongtrack], dims=["labels", "dist_alongtrack"], attrs=attrs)
    return da

def organize_data(filenames, beams):
    ta = np.zeros((len(filenames),4,9), dtype=object)
    loc = "Lake Louise, AK"
    data_dict = {}
    for ii in range(len(filenames)):
        with h5py.File(filenames[ii], 'r') as f:
            sc_orient = f["orbit_info"]["sc_orient"]
            if sc_orient == 0 and 'r' in beam:
                print("Orientation is backwards. Strong beams on left. Try again.")
                return

            ta[ii,3,0] = f["ancillary_data"]["start_rgt"][0]

            for jj in range(len(beams)):
                try:
                    #print(filenames[ii] + ", " + beams[jj])

                    ta[ii,jj,0] = f[beams[jj]]['heights']['lon_ph'][:]    # photon longitude (x)
                    ta[ii,jj,1] = f[beams[jj]]['heights']['lat_ph'][:]    # photon latitude  (y)
                    ta[ii,jj,2], ta[ii,jj,3] = coords_trans(list(ta[ii,jj,0]), list(ta[ii,jj,1])) # convert lon,lat to x,y in UTM 10
                    ta[ii,jj,4] = f[beams[jj]]['heights']['h_ph'][:]        # photon elevation (z), in m
                    ta[ii,jj,5] = f[beams[jj]]['heights']['signal_conf_ph'][:,2] # photon quality, 0 = noise, 1 = Transmit Echo Pulse (TEP), 2 = low, 3 = medium, 4 = high
                    ta[ii,jj,6] = f[beams[jj]]['heights']['signal_conf_ph'][:,3]
                    ta[ii,jj,7] = f[beams[jj]]['heights']['signal_conf_ph'][:,4]
                    ta[ii,jj,8] = make_dist_alongtrack(f[beams[jj]]['geolocation']['segment_ph_cnt'][:],  # photon count in each segment, in m
                                                       f[beams[jj]]['geolocation']['segment_length'][:],  # horizontal of each segment, in m, 
                                                       f[beams[jj]]['heights']['dist_ph_along'][:]  # photon horizontal distance from the beginning of the parent segment, in m
                                                        )   # distance along track for each photon, in m
                    #create DataArray
                    da = create_da(ta[ii,jj,0], ta[ii,jj,1], ta[ii,jj,2], ta[ii,jj,3], ta[ii,jj,4], ta[ii,jj,5], ta[ii,jj,6], ta[ii,jj,7], ta[ii,jj,8], filenames[ii], loc, ta[ii,3,0], beams[jj])
                    print(beams[jj] + " in file " + filenames[ii] + " was placed into a DataArray")
                    tkey1 = str(ta[ii,3,0])
                    tkey2 = beams[jj]
                    if tkey1 in data_dict:
                        data_dict[tkey1].update({tkey2: da})
                    else:
                        data_dict[tkey1] = {tkey2: da}
                    
                except:
                    print(beams[jj] + " in file " + filenames[ii] + " has no data")

    return data_dict


# qual values: -2=TEP, -1=no landform associated, 0=land, 1=ocean, 2=sea ice, 3=land ice, 4=inland water
# confidence levels: 0=noise, 1=TEP, 2=low, 3=mid, 4=high

#implement plotting of specific confidence levels, not all 3 no matter what confs parameter says!

def plot_beams(data, confs=[4], dif=True, landforms=[0,1,2,3,4,5]):
    num_beams = sum(len(v) for v in data.values())
    landform_names = ['n/a', 'land', 'ocean', 'sea ice', 'land ice', 'inland water']
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:black"]
    if dif==True:
        ii = 0
        jj = 0
        fig, axs = plt.subplots(num_beams, len(landforms), figsize=(20, num_beams*2+1), constrained_layout=True)
        for v1 in data.values():
            for v2 in v1.values():
                for jj in range(len(landforms)):
                    v2.loc['h'].where(v2.loc['q2'] == landforms[jj]).plot.line('.', ax=axs[ii,jj], markersize=4, linestyle='None', color=colors[0])
                    v2.loc['h'].where(v2.loc['q3'] == landforms[jj]).plot.line('.', ax=axs[ii,jj], markersize=4, linestyle='None', color=colors[1])
                    v2.loc['h'].where(v2.loc['q4'] == landforms[jj]).plot.line('.', ax=axs[ii,jj], markersize=4, linestyle='None', color=colors[2])
                    axs[ii,jj].set_title(landform_names[jj])
                    axs[ii,jj].set_ylabel((v2.attrs['RGT'], v2.attrs['Beam']))
                    jj+=1
                ii+=1
        fig.legend(["low conf", "med conf", "high conf"])
    else:
        ii = 0
        jj = 0
        fig, axs = plt.subplots(num_beams, 1, figsize=(20, num_beams*2+1), constrained_layout=True)
        for v1 in data.values():
            for v2 in v1.values():
                for jj in range(len(landforms)):
                    v2.loc['h'].where((v2.loc['q2'] == landforms[jj]) | (v2.loc['q3'] == landforms[jj]) | (v2.loc['q4'] == landforms[jj])).plot.line('.', ax=axs[ii], markersize=4, linestyle='None', color=colors[jj])
                    axs[ii].set_title((v2.attrs['RGT'], v2.attrs['Beam']))
                    axs[ii].set_ylabel("Elevation [m]")
                    jj+=1
                ii+=1
        fig.legend([landform_names[i] for i in landforms])