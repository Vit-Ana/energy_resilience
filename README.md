# Solar Power Siting in Ukraine: Risk-Aware Energy Planning in War-Affected Zones
## 1. Purpose of the Analysis

This project evaluates the viability of building solar power plants in Ukraine, accounting for safety concerns related to the ongoing war. The core aim is to identify areas that are far enough from recent attacks to be considered “relatively safe,” and then estimate how much land and investment would be needed to replace the lost capacity of the Zaporizhzhia Nuclear Power Plant using solar energy. The analysis also includes a financial assessment through Net Present Value (NPV) calculations and estimates an insurance premium reflecting the conflict risk.

## 2. Data Sources & How to Obtain Them

**a. ACLED Warfare Events**
- Website: ACLED Ukraine Conflict Monitor
- Data Description: Contains attacks event data with precise geographic coordinates and timestamps.
- Manual Download: Download the .xls file by clicking "Download file" `Ukraine & the Black Sea (18 April 2025)`.
- Converted to CSV (used in scripts): `Ukraine_Infrastructure_Tags_2025-03-26.csv`

**b. Ukraine Administrative Boundaries**
- File Type: geopackage (.gpkg).
- Source: GADM.
- Usage: Used to define the national borders and calculate the country’s total land area.

## 3. Scripts and Workflow
### Script 1: ```01_map_download.py```
Loads Ukraine map as a geopackage.

### Script 2: ```02_ukr_map.py```
Converts the attack coordinates into point geometries.\
Projects all data to a metric coordinate system for distance-based buffer calculations.

### Script 3: ```03_attacks_buffers.py```
Creates a 20km buffer around all attack locations.\
Creates a second ring buffer between 20km and 40km around attacks.\
Subtracts the risky zones from the national territory to isolate “relatively safe” land.\
All area-based computations use projected coordinates: EPSG:32636.\
Uploading the saved geopackage file to QGIS.

**Map of Attacks (Using QGIS)**
![Map of Attacks](map_buffers.png)

### Script 4: ```04_capacity_SPP_and_WPP.py```
Calculates the area of the safe territory.\
Applies a capacity factor (0.1) to estimate usable area for solar farms and 0.35 for wind farms.\
Estimates annual energy production.

### Script 5: ```05_area_SPP_WPP.py```
Computes potential installed solar capacity to substitute Zaporizhzhia NPP (6000MW) capacity that was occupied by the Russian forces.\
Applies a capacity factor (0.1) to estimate usable area for solar farms and 0.35 for wind farms.\
Calculates the percentage of the remaining safe area needed for solar and wind power plants installation. 

### Script 6: ```06_npv+insurance.py```
Estimates the Net Present Value (NPV) of installing domestic and industrial solar power plants in the safe zone.\
Estimates a war-related risk insurance premium based on exposed vs. safe land.

### Script 7: ```07_financial_model.py```
Builds a simplified financial model to estimate the NPV of solar power plant deployment in safe zones.\
Incorporates assumptions for CAPEX, OPEX, electricity prices, and a discount rate.\
Includes a comparative analysis against the Khmelnytska Nuclear Power Plant (2000 MW) to contextualize the economic feasibility.

## 4. Additional Files
```attacks.gpkg```: GeoPackage storing processed buffer layers.


## 5. Results Summary
- Safe Area Identified: Approximately 169773.40 km² remains outside the risk zones.

- Solar Substitution Potential: Only 0.71% or 1200 km² of the relatively safe area is needed to match the 6 GW capacity of Zaporizhzhia NPP.

- Annual Production: Estimated 37180.37 GWh GWh/year if only the fraction of 0.005 of available land is used.

- NPV: Estimated at $15 billion over the plant lifetime, assuming a 7% discount rate and 25-year horizon.

- Insurance Premium Estimate: Based on territorial exposure, the war-risk premium is modeled as a percentage of capital investment and may range from $240 million to $480 million.

## How to Reproduce
1. Download raw datasets as described above.

2. Follow the script order:
    
    > 01_map_download.py\
    02_ukr_map.py\
    03_attacks_buffers.py\
    04_capacity_SPP_and_WPP.py\
    05_area_SPP_WPP.py\
    06_npv+insurance.py\
    07_financial_model.py

3. Ensure all files are saved in the correct directories before running each notebook.

4. You may need to install the following Python packages:
```pip install geopandas pandas numpy matplotlib shapely openpyxl```