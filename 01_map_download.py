#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 13:43:50 2025

@author: vitana
"""

# --- Downloading the map with Ukraine's country boundaries and regions ---
import requests

url = "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_UKR.gpkg"
filename = "gadm41_UKR.gpkg"

print(f"Attempting to download '{filename}' from '{url}'...")

try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # raising an exception for bad status codes

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filtering out keep-alive new chunks
                file.write(chunk)

    print(f"\nSuccessfully downloaded '{filename}'.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the download: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")