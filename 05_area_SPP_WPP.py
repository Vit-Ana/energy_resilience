#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 12:12:51 2025

@author: vitana
"""

import geopandas as gpd
    
#%%
#reading the file with the map of the territory of Ukraine, except the occupied regions
#as well as those close to the occupied areas and the frontline
out_file = "map_of_attacks.gpkg"
#reading the buffers    
buffer_risky = gpd.read_file(out_file, layer="buffer_risky")
country_area = gpd.read_file(out_file, layer="not_occupied")

#changing crs for computation purposes
target_crs = "EPSG:32636"
buffer_risky = buffer_risky.to_crs(target_crs)
country_area = country_area.to_crs(target_crs)


#%%

#dissolving geometries to make a single polygon for subtraction
risky_union = buffer_risky.unary_union
country_union = country_area.unary_union

#creating GeoSeries for area calculation
risky_zone = gpd.GeoSeries([risky_union], crs=country_area.crs)
country_zone = gpd.GeoSeries([country_union], crs=country_area.crs)

#calculating areas
country_area_m2 = country_zone.area.sum() # total country area from the map(some regions excluded)
risky_area_m2 = risky_zone.area.sum() # area of the territory where it's not recommended 
                                      # to build a power plant due to constant shelling
safe_area_m2 = country_area_m2 - risky_area_m2 # recommended area

# Print results
print(f"Total area (not_occupied): {country_area_m2 / 1e6:.2f} km²")
print(f"Risky buffer area (no overlap): {risky_area_m2 / 1e6:.2f} km²")
print(f"Safe installable area: {safe_area_m2 / 1e6:.2f} km²")


#%%

# --- Function to calculate required area and percentage ---
def calculate_energy_area(required_MW, area_per_MW, capacity_factor, safe_area_m2):
    adjusted_MW = required_MW / capacity_factor
    required_area_m2 = adjusted_MW * area_per_MW
    percentage_needed = (required_area_m2 / safe_area_m2) * 100
    return required_area_m2, percentage_needed

#%%
# --- Solar Calculation ---
solar_required_MW = 6000
solar_area_per_MW = 20000  # m² per MW (2 ha/MW as per turbine spacing)
solar_capacity_factor = 0.1 # the lowest factor for solar 

solar_area_m2, solar_percentage = calculate_energy_area(
    solar_required_MW, solar_area_per_MW, solar_capacity_factor, safe_area_m2
)

#%%
# --- Wind Calculation ---
wind_required_MW = 6000
wind_area_per_MW = 80000  # m² per MW (8 ha/MW as per turbine spacing)
wind_capacity_factor = 0.35  # a factor for wind

wind_area_m2, wind_percentage = calculate_energy_area(
    wind_required_MW, wind_area_per_MW, wind_capacity_factor, safe_area_m2
)

#%%
# --- Output ---
print("\n--- Potential in the Area Outside the Buffers ---")
print("\n[ Solar ]")
print(f"Area needed for {solar_required_MW}MW: {solar_area_m2 / 1e6:.2f} km²")
print(f"Percentage of safe land needed: {solar_percentage:.2f}%")

print("\n[ Wind ]")
print(f"Area needed for {wind_required_MW}MW: {wind_area_m2 / 1e6:.2f} km²")
print(f"Percentage of safe land needed: {wind_percentage:.2f}%")


#%%
#saving as a new layer
safe_geom = country_union.difference(risky_union)
safe_zone_gdf = gpd.GeoDataFrame(geometry=[safe_geom], crs=country_area.crs)
safe_zone_gdf.to_file(out_file, layer="safe_install_zone")
                      
                      
                      