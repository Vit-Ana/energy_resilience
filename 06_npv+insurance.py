#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 16:58:25 2025

@author: vitana
"""

#  --- NPV Equations ---
# 1. Quantity of power plants
def calculate_station_count(target_mw, station_capacity_kw):
    return int((target_mw * 1000) / station_capacity_kw)

# 2. NPV calculation
def calculate_npv(initial_investment, annual_cashflow, discount_rate, years):
    npv = -initial_investment
    for t in range(1, years + 1):
        npv += annual_cashflow / ((1 + discount_rate) ** t)
    return round(npv, 2)

# 3. Insurance premium depending on the region
def calculate_insurance_premium(project_cost, risk_level='safe'):
    risk_levels = {
        'safe': (0.05, 0.1),    # 5–10%
        'risky': (0.2, 0.3)     # 20–30%
    }
    low, high = risk_levels[risk_level]
    return round(project_cost * low, 2), round(project_cost * high, 2)


#%%
#  --- NPV Calculations ---
# Defining parameters
target_mw = 6000  # total MW needed

# Home solar
home_capacity_kw = 10  # typical rooftop system
home_cost = 9000  # USD
home_annual_profit = 1400  # e.g., savings from bills
home_years = 20
home_discount = 0.08

# Industrial solar
industrial_capacity_kw = 500  # small utility-scale system
industrial_cost = 400000  # USD avarage
industrial_annual_profit = 120000 # USD avarage 
industrial_years = 25
industrial_discount = 0.08

# Calculating station counts
home_count = calculate_station_count(target_mw, home_capacity_kw)
industrial_count = calculate_station_count(target_mw, industrial_capacity_kw)

# NPV
npv_home = calculate_npv(home_cost, home_annual_profit, home_discount, home_years)
npv_industrial = calculate_npv(industrial_cost, industrial_annual_profit, industrial_discount, industrial_years)

# Insurance (safe region)
home_insurance = calculate_insurance_premium(home_cost, 'safe')
industrial_insurance = calculate_insurance_premium(industrial_cost, 'safe')

# Total costs
total_home_cost = home_count * home_cost
total_industrial_cost = industrial_count * industrial_cost

# Total insurance support
total_home_insurance = (home_insurance[0] * home_count, home_insurance[1] * home_count)
total_industrial_insurance = (industrial_insurance[0] * industrial_count, industrial_insurance[1] * industrial_count)

# Total NPVs
total_npv_home = home_count * npv_home
total_npv_industrial = industrial_count * npv_industrial

# Printing results
print("--- Home-scale SPPs ---")
print(f"Number of stations needed: {home_count}")
print(f"NPV per unit: ${npv_home}")
print(f"Insurance premium (safe): from ${home_insurance[0]} to ${home_insurance[1]}")

print("\n--- Industrial-scale SPPs ---")
print(f"Number of stations needed: {industrial_count}")
print(f"NPV per unit: ${npv_industrial}")
print(f"Insurance premium (safe): from ${industrial_insurance[0]} to ${industrial_insurance[1]}")

print("\n--- Total Program Estimates ---")
print(f"Total cost (home systems): ${total_home_cost:,.0f}")
print(f"Total cost (industrial systems): ${total_industrial_cost:,.0f}")
print(f"Total insurance support (home systems): from ${total_home_insurance[0]:,.0f} to ${total_home_insurance[1]:,.0f}")
print(f"Total insurance support (industrial systems): from ${total_industrial_insurance[0]:,.0f} to ${total_industrial_insurance[1]:,.0f}")
print(f"Total NPV (home systems): ${total_npv_home:,.0f}")
print(f"Total NPV (industrial systems): ${total_npv_industrial:,.0f}")
