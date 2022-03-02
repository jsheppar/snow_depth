#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 20:01:01 2021

@author: jsheppard
"""

# IceSAT2 test script
#%% 0. Import Packages
import icepyx as ipx

import numpy as np
import hvplot.xarray
import pandas as pd

import h5py
import os, json
from pprint import pprint

import matplotlib.pyplot as plt
import re
import geopandas as gpd
import rioxarray

#%%
louise_Jan = ipx.Query(
    "ATL03",
    [-146.35, 62.18, -146.30, 62.21],
    ["2020-01-01", "2020-01-30"],
    start_time="00:00:00",
    end_time="23:59:59",
)

louise_Apr = ipx.Query(
    "ATL03",
    [-146.35, 62.18, -146.30, 62.21],
    ["2020-03-01", "2020-04-30"],
    start_time="00:00:00",
    end_time="23:59:59",
)

#%%
print(list(set(louise_Jan.avail_granules(cycles=True)[0])))  # region.cycles
print(list(set(louise_Apr.avail_granules(tracks=True)[0])))  # region.tracks

#%% DOESNT WORK
louise_Apr.visualize_spatial_extent()

#%%
earthdata_uid = "jsheppar"
email = "jsheppar@uoregon.edu"
louise_Jan.earthdata_login(earthdata_uid, email)

#%%
louise_Apr.earthdata_login(earthdata_uid, email)
#%%
# region_a.show_custom_options(dictview=True)

#%%
a = louise_Jan.order_vars.avail()
b = louise_Apr.order_vars.avail()
#%%
louise_Jan.order_vars.append(var_list=["h_ph", "lat_ph", "lon_ph", "ref_azimuth"])
louise_Apr.order_vars.append(var_list=["h_ph", "lat_ph", "lon_ph", "ref_azimuth"])

#%%
louise_Jan.subsetparams(Coverage=louise_Jan.order_vars.wanted)
louise_Apr.subsetparams(Coverage=louise_Apr.order_vars.wanted)
#%%
louise_Jan.reqparams["request_mode"] = "async"
louise_Jan.order_granules()
louise_Jan.download_granules("./l_louise_data/Jan")

louise_Apr.reqparams["request_mode"] = "async"
louise_Apr.order_granules()
louise_Apr.download_granules("./l_louise_data/Apr")
#%%
fn1 = "./l_louise_data/Jan/processed_ATL03_20200109032938_02050603_004_01.h5"
fn2 = "./l_louise_data/Apr/processed_ATL03_20200414112020_02890705_004_01.h5"


def visit_func(name, node):
    # print("Full object pathname is:", node.name)
    if isinstance(node, h5py.Dataset):
        print("Object:", name, "is a Dataset\n")
        if "h_ph" in name or "orbit_info/sc_orient" == name:
            my_paths.append(name)
            my_tracks.append(name[0:4])


def create_df(file):
    with h5py.File(file, "r") as h5r:
        h5r.visititems(visit_func)
        temp_dict = {track: h5r[path] for track, path in zip(my_tracks, my_paths)}
        return pd.DataFrame(dict([(k, pd.Series(v)) for k, v in temp_dict.items()]))


my_paths, my_tracks = [], []
louise_Jan_df = create_df(fn1)
my_paths, my_tracks = [], []
louise_Apr_df = create_df(fn2)

#orientation 1: forward, strong on right
#orientation 0: backwards, strong on left
#%%
print(louise_Apr_df)
fig, ax = plt.subplots()
ax.plot(louise_Apr_df['gt1r'], 'tab:blue')
ax.plot(louise_Jan_df['gt2r'], 'tab:cyan')
ax.plot(louise_Apr_df['gt1r']-louise_Jan_df['gt2r'], 'tab:red')
ax.plot(np.zeros(len(louise_Apr_df['gt1r'])), 'k')
ax.set_title("Photon Elevation for Strong Beams Over Lake Lousie")
ax.legend(["Apr", "Jan", "Apr-Jan", "zero"])
#fig.show()


#slope of beams 1,2,3, check for slope on lake