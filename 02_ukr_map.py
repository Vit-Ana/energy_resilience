#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 08:59:00 2025

@author: vitana
"""

import geopandas as gpd
import fiona

out_file_1 = "ukr_map.gpkg"
out_file_2 = "map_of_attacks.gpkg"

# --- Input File ---
ukr_map = 'gadm41_UKR.gpkg'
#listing the layers
layers = fiona.listlayers(ukr_map)
print( f'Layers in {ukr_map}:', layers )

#%%
#reading each layer into a separate dataframe
country = gpd.read_file(ukr_map,layer='ADM_ADM_0')
oblast = gpd.read_file(ukr_map,layer='ADM_ADM_1')
region  = gpd.read_file(ukr_map,layer='ADM_ADM_2')
oblast.to_csv('oblast.csv')
region.to_csv('region.csv')

#saving a layer in the output file
country = country.to_file(out_file_1,layer='borders')

#%%
#changing the oblast column, deleting null values and changing names
oblast['NAME_1'] = oblast['NAME_1'].replace(r"Kiev", "Kyiv", regex=True)
oblast['NAME_1'] = oblast['NAME_1'].str.replace("'", "", regex=False)
oblast['NL_NAME_1'] = oblast['NL_NAME_1'].replace({"NA": "Львівська"})
oblast = oblast.drop(columns=['VARNAME_1', 'CC_1', 'ISO_1'])

#saving a layer in the output file
oblast.to_file(out_file_1,layer='oblast')

#%%
#changing the oblast column, deleting columns with null values and changing names
for col in region.columns:
    if region[col].dtype == 'object':
        region[col] = region[col].str.replace("'", "")
region.columns.to_list
columns_to_drop = ['NL_NAME_2', 'CC_2']
region = region.drop(columns=columns_to_drop)

#saving a layer in the output file
region.to_file(out_file_1,layer='raion')


#%%
#adding the oblast boundaries to the attacks map without the regions close to the frontline 
#(Kharkiv, Luhansk, Donetsk, Zaporizhia, Kherson and occupied since 2014 Crimea and Sevastopol) 
attacks = gpd.read_file(out_file_2)
region_1 = region.copy()

#dropping the occupied territories and close to the frontline regions
region_1 = region_1.query(
    'NAME_1 != "Kharkiv" and '
    'NAME_1 != "Luhansk" and '
    'NAME_1 != "Donetsk" and '
    'NAME_1 != "Zaporizhia" and '
    'NAME_1 != "Kherson" and '
    'NAME_1 != "Crimea" and NAME_1 != "Sevastopol"'
)

#saving to the map of attacks
region_1.to_file(out_file_2, layer="not_occupied")


