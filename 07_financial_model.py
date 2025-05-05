#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 19:53:43 2025

@author: vitana
"""

import pandas as pd
import matplotlib.pyplot as plt


# --- Discounted Cash Flow --- 
def discounted_cash_flow(revenue, opex, years, discount_rate, start_year):
    return sum(
        ((revenue - opex) / (1 + discount_rate) ** (y + start_year))
        for y in range(years)
    )

def calculate_npv(capex, revenue, opex, years, discount_rate, start_year,
                  insurance=0, risk_probability=0):
    total_cost = capex + insurance * capex
    dcf = discounted_cash_flow(revenue, opex, years, discount_rate, start_year)
    expected_loss = risk_probability * dcf  # risk of full loss
    return dcf - total_cost - expected_loss

def lcoe(capex, opex, energy_generated):
    return (capex + opex * len(energy_generated)) / sum(energy_generated)


# --- Simulation Scenarios ---
def simulate_power_plant(capacity_mw, capex, capacity_factor, lifetime_years,
                         price_per_mwh, opex_per_year, discount_rate,
                         construction_years, insurance=0, risk_probability=0,
                         name="Power Plant"):
    operational_years = lifetime_years
    annual_energy = capacity_mw * 8760 * capacity_factor
    revenue = price_per_mwh * annual_energy
    opex = opex_per_year

    npv = calculate_npv(
        capex, revenue, opex, operational_years, discount_rate,
        start_year=construction_years,
        insurance=insurance,
        risk_probability=risk_probability
    )

    energy_profile = [annual_energy] * operational_years
    cost_per_mwh = lcoe(capex, opex, energy_profile)
    total_revenue = revenue * operational_years

    return {
        "Name": name,
        "Capacity (MW)": capacity_mw,
        "Construction Delay (yrs)": construction_years,
        "CAPEX ($)": capex,
        "Insurance (%)": insurance * 100,
        "Risk (%)": risk_probability * 100,
        "LCOE ($/MWh)": round(cost_per_mwh, 2),
        "NPV (in million $)": round(npv/1e6, 2),
        "Total Revenue (in million $)": round(total_revenue/1e6, 2)
    }


#%%
# --- Simulation Scenario for 2 generation of SPPs one after another ---
def simulate_solar_two_generations(capacity_mw, capex, capacity_factor, lifetime_years,
                         price_per_mwh, opex_per_year, discount_rate,
                         construction_years, insurance=0, risk_probability=0,
                         name="Power Plant"):
    total_npv = 0
    total_revenue = 0
    total_energy = 0

    for gen in range(2):
        start_year = construction_years + gen * lifetime_years
        operational_years = lifetime_years if gen == 0 else 15  # only up to 40 yrs total
        annual_energy = capacity_mw * 8760 * capacity_factor
        revenue = price_per_mwh * annual_energy
        opex = opex_per_year

        npv = calculate_npv(
            capex, revenue, opex, operational_years, discount_rate,
            start_year=start_year,
            insurance=insurance,
            risk_probability=risk_probability
        )
        total_npv += npv
        total_revenue += revenue * operational_years
        total_energy += annual_energy * operational_years

    lcoe_value = (2 * capex + 2 * opex_per_year * 25) / total_energy

    return {
        "Name": name,
        "Capacity (MW)": capacity_mw,
        "Construction Delay (yrs)": construction_years,
        "CAPEX ($)": capex,
        "Insurance (%)": insurance * 100,
        "Risk (%)": risk_probability * 100,
        "LCOE ($/MWh)": round(lcoe_value, 2),
        "NPV (in million $)": round(total_npv/1e6, 2),
        "Total Revenue (in million $)": round(total_revenue/1e6, 2)
    }

#%%
# Simulating results for individual plants and adding to the results list    

results = []
price_per_mwh = 143.44
discount_rate = 0.07

results.append(simulate_power_plant(
    capacity_mw=2200,
    capex=3831395200,
    capacity_factor=0.85,
    lifetime_years=40,
    price_per_mwh=price_per_mwh,
    opex_per_year=200_000_000,
    discount_rate=discount_rate,
    construction_years=5,
    insurance=0.1,
    risk_probability=0.5,
    name="Khmelnytska NPP (5 yr delay)"
))

results.append(simulate_power_plant(
    capacity_mw=2000,
    capex=1_760_000_000,
    capacity_factor=0.2,
    lifetime_years=25,
    price_per_mwh=price_per_mwh,
    opex_per_year=50_000_000,
    discount_rate=discount_rate,
    construction_years=1,
    insurance=0.01,
    risk_probability=0.01,
    name="Solar Plant Equivalent"
))

results.append(simulate_solar_two_generations(
    capacity_mw=2200,
    capex=1_760_000_000,
    capacity_factor=0.2,
    lifetime_years=25,
    price_per_mwh=price_per_mwh,
    opex_per_year=50_000_000,
    discount_rate=discount_rate,
    construction_years=1,  # 1 year construction delay
    insurance=0.01,
    risk_probability=0.01,
    name="Solar Power Plant – Two Generations"
))

results.append(simulate_power_plant(
    capacity_mw=2200,
    capex=5_700_000_000,
    capacity_factor=0.85,
    lifetime_years=40,
    price_per_mwh=price_per_mwh,
    opex_per_year=200_000_000,
    discount_rate=discount_rate,
    construction_years=8,
    insurance=0.1,
    risk_probability=0.5,
    name="Khmelnytska NPP (8 yr delay)"
))

results.append(simulate_power_plant(
    capacity_mw=2200,
    capex=7_600_000_000,
    capacity_factor=0.85,
    lifetime_years=40,
    price_per_mwh=price_per_mwh,
    opex_per_year=200_000_000,
    discount_rate=discount_rate,
    construction_years=10,
    insurance=0.1,
    risk_probability=0.5,
    name="Khmelnytska NPP (10 yr delay)"
))


comparison = pd.DataFrame(results)

#%%
# Plotting the NPVs
plt.rcParams['figure.dpi'] = 300
colors = ['mediumpurple', 'gold', 'mediumseagreen', 'plum', 'olivedrab']
plt.figure(figsize=(12, 8))
plt.barh(comparison['Name'], comparison['NPV (in million $)'], color=colors)
plt.xlabel('NPV (in million $)', fontsize=16)
plt.ylabel('Power Plant Type', fontsize=16)
plt.title('NPV Comparison for Solar and Nuclear Power Plants', fontsize=20)
plt.tight_layout()
plt.show()
plt.savefig("npv_comparison_plot.png")


