#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 09:23:45 2025

@author: vitana
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

#reading downloaded from https://acleddata.com/ukraine-conflict-monitor/#dash
df = pd.read_csv('Ukraine_Infrastructure_Tags_2025-03-26.csv')
# dropping locations that are occupied by the Russian forces
df = df.drop(df[df['LOCATION'].str.contains('BLACK SEA', case=False, na=False)].index)
df = df.drop(df[df['ADMIN1'].str.contains('DONETSK', case=False, na=False)].index)
df = df.drop(df[df['ADMIN1'].str.contains('LUHANSK', case=False, na=False)].index)
df = df.drop(df[df['ADMIN1'].str.contains('CRIMEA', case=False, na=False)].index)


#%%

# --- plotting the buffers ---

out_file = "map_of_attacks.gpkg"
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']), crs="EPSG:4326")
gdf = gdf.to_crs(epsg=32636)

#%%

#creating a geopackage file with buffers with different radii
#setting the radius in metres
radius = [20000, 40000]
colors = ['red', 'green']
layer_names = ["buffer_risky", "buffer_safe"]

#creating a list to hold the GeoDataFrames for each layer
ring_layers = []
last_buffer = None

for i, r in enumerate(radius):
    current_buffer = gdf.buffer(r)
    buffer_gdf = gpd.GeoDataFrame(geometry=current_buffer, crs=gdf.crs)

    if last_buffer is None:
        ring_layers.append(buffer_gdf)
    else:
        # Calculate the area between the current buffer and the last buffer
        annulus = current_buffer.difference(last_buffer)
        annulus_gdf = gpd.GeoDataFrame(geometry=annulus, crs=gdf.crs)
        ring_layers.append(annulus_gdf)

    last_buffer = current_buffer

#checking if file already exists and removing the duplicate, saving as geopkg
if os.path.exists(out_file):
    os.remove(out_file)

#saving each ring as a separate layer in the GeoPackage
for i, ring_gdf in enumerate(ring_layers):
    ring_gdf.to_file(out_file, layer=layer_names[i], driver="GPKG")


#%%
# --- Map with <20km and 20-40 km Buffers around the Attack Sites ---
#plotting the color-coded rings 
reversed_indices = [1, 0]

fig1, ax1 = plt.subplots(dpi=300)
gdf.plot(color="tan", ax=ax1)

for i in reversed_indices:
    if i < len(ring_layers):
        ring_layers[i].plot(color=colors[i], ax=ax1, label=layer_names[i])

ax1.axis("off")
ax1.legend()
fig1.savefig("attacks_buffers.png")
plt.show()














