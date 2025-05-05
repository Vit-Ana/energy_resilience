#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 20:14:52 2025

@author: vitana
"""


import geopandas as gpd

#%%
#reading the data files of the territories for estimate power plant capacity  
out_file = "map_of_attacks.gpkg"
target_crs = "EPSG:32636"
buffer_risky = gpd.read_file(out_file, layer="buffer_risky").to_crs(target_crs)
buffer_safe = gpd.read_file(out_file, layer="buffer_safe").to_crs(target_crs)
country_area = gpd.read_file(out_file, layer="not_occupied").to_crs(target_crs)

#%%
# --- Parameters and conversion factors ---

available_land_solar = 0.005  # Fraction of land available for solar
available_land_wind = 0.1    # Fraction of land available for wind

solar_area_per_MW_ha = 2      # Solar area per MW in hectares
solar_capacity_factor = 0.1    # Solar capacity factor
ha_to_sqm = 10000             # Conversion from hectares to square meters
solar_area_per_MW_sqm = solar_area_per_MW_ha * ha_to_sqm  # Solar area per MW in square meters

wind_area_per_turbine_ha = 2  # Wind area per turbine in hectares
wind_capacity_per_turbine_MW = 3  # Wind capacity per turbine in MW
wind_capacity_factor = 0.25   # Wind capacity factor
turbine_exclusion_radius_m = 500  # Radius of exclusion for wind turbines in meters

#function for solar capacity
def estimate_solar_capacity(area_sqm):
    available_area_sqm = area_sqm * available_land_solar  # Available land area for solar
    return available_area_sqm / solar_area_per_MW_sqm * 0.001  # Convert to GW

#function for computing wind capacity
def estimate_wind_capacity(area_sqm):
    available_area_sqm = area_sqm * available_land_wind  # Available land area for wind
    spacing = 5 * turbine_exclusion_radius_m  # Spacing between turbines
    area_per_turbine = (2 * turbine_exclusion_radius_m + spacing)**2  # Area per turbine
    num_turbines = int(available_area_sqm / area_per_turbine)  # Number of turbines
    return num_turbines, num_turbines * wind_capacity_per_turbine_MW * 0.001  # Return number of turbines and wind capacity in GW

def estimate_annual_production(capacity_gw, capacity_factor):
    return capacity_gw * capacity_factor * 365 * 24  # Convert to GWh

#%%
# dissolving geometries to make a single polygon for subtraction
risky_union = buffer_risky.unary_union
country_union = country_area.unary_union

# creating GeoSeries for consistent area calculation
risky_zone = gpd.GeoSeries([risky_union], crs=country_area.crs)
country_zone = gpd.GeoSeries([country_union], crs=country_area.crs)

# calculating areas
country_area_m2 = country_zone.area.sum()  # Total country area in square meters
risky_area_m2 = risky_zone.area.sum()  # Total risky area in square meters
safe_area_m2 = country_area_m2 - risky_area_m2  # Safe area in square meters

print(f"Total installable safe area: {safe_area_m2 / 1e6:.2f} km²")

#%%
# estimating potential capacities and production in the safe area
solar_safe = estimate_solar_capacity(safe_area_m2)  # Pass the numeric area value
wind_turbines_safe, wind_safe = estimate_wind_capacity(safe_area_m2)  # Pass the numeric area value
annual_solar_safe = estimate_annual_production(solar_safe, solar_capacity_factor)
annual_wind_safe = estimate_annual_production(wind_safe, wind_capacity_factor)

print("\n--- Potential in the SAFE AREA ---")
print(f"Solar capacity: {solar_safe:.2f} GW")
print(f"Annual solar production: {annual_solar_safe:.2f} GWh")
print(f"Wind turbines: ~{wind_turbines_safe}")
print(f"Wind capacity: ~{wind_safe:.2f} GW")
print(f"Annual wind production: ~{annual_wind_safe:.2f} GWh")
