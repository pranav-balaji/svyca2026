# SolarSchools USA: API & Data Services Reference Guide
**Author:** Pranav Balaji | **Competition:** SVYCA Youth For Earth Hackathon @ Stanford Climate Week  

---

## Overview

SolarSchools USA integrates three external web services and APIs to model solar physics, satellite imagery, and campus geospatial boundaries:

1. **U.S. Department of Energy / National Laboratory of the Rockies (NLR) PVWatts v8 REST API** — Physical solar AC generation modeling.
2. **Esri ArcGIS REST Map Service** — High-resolution aerial satellite imagery tiles.
3. **OpenStreetMap Direct Map API** — Surface parking lot polygon extraction.

This document details the exact endpoints, request parameters, JSON response schemas, error-handling fallbacks, and a speaking guide for presenting these technical details to judges.

---

## 1. Solar Physics API: NLR / DOE PVWatts v8

* **Provider:** National Laboratory of the Rockies (NLR / formerly NREL), U.S. Department of Energy
* **Official Endpoint:** `https://developer.nlr.gov/api/pvwatts/v8.json`
* **HTTP Method:** `GET`
* **Implementation File:** [`core/solar_engine.py`](./core/solar_engine.py)

### Why developer.nlr.gov?
> **Key Technical Note for Judges:** In May 2026, the U.S. Department of Energy reorganized the National Renewable Energy Laboratory (NREL) under the National Laboratory of the Rockies (NLR). The legacy domain `developer.nrel.gov` was retired and replaced by `developer.nlr.gov`. Our application connects directly to the active federal endpoint.

### Request Parameters

| Parameter | Type | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `api_key` | string | `DEMO_KEY` | Federal developer key for rate-limiting and authentication. |
| `lat` | float | `37.4358` | Latitude in decimal degrees (WGS 84 / EPSG:4326). |
| `lon` | float | `-122.1553` | Longitude in decimal degrees (WGS 84 / EPSG:4326). |
| `system_capacity` | float | `608.4` | Nameplate DC capacity of the canopy array in kilowatts (kW). |
| `azimuth` | float | `180` | Array orientation in degrees ($180^\circ$ = True South for maximum solar harvest in the Northern Hemisphere). |
| `tilt` | float | `10` | Fixed tilt angle of the canopy canopy structure ($10^\circ$ standard drainage and solar collection pitch). |
| `array_type` | integer | `2` | Mounting geometry ($2$ = Fixed roof mount / canopy mount). |
| `module_type` | integer | `1` | Photovoltaic module technology ($1$ = Premium Monocrystalline Silicon, ~20% efficiency). |
| `losses` | float | `14.0` | Total system derate percentage (covers soiling, inverter conversion efficiency, DC/AC wiring resistance, and thermal mismatch). |

### Sample HTTP Request
```http
GET https://developer.nlr.gov/api/pvwatts/v8.json?api_key=DEMO_KEY&lat=37.4358&lon=-122.1553&system_capacity=608.4&azimuth=180&tilt=10&array_type=2&module_type=1&losses=14.0
```

### Response Schema (JSON)
The federal API returns a nested JSON response. Our engine extracts three primary output keys from `outputs`:

```json
{
  "version": "8.0.0",
  "inputs": {
    "system_capacity": "608.4",
    "lat": "37.4358",
    "lon": "-122.1553"
  },
  "outputs": {
    "ac_annual": 1227738.4,
    "capacity_factor": 23.04,
    "ac_monthly": [
      52800.2, 68700.5, 91400.1, 119200.3, 140300.8, 149500.4,
      148200.1, 137400.6, 118900.2, 92100.5, 61200.3, 48035.4
    ],
    "solrad_annual": 5.48
  }
}
```

* **`ac_annual`:** First-year total alternating-current (AC) electricity produced by the array in kilowatt-hours (kWh).
* **`capacity_factor`:** Percentage of the year the system produces at full rated nameplate capacity (typically 20%–24% in California).
* **`ac_monthly`:** Array of 12 floats representing estimated AC kilowatt-hours produced each calendar month from January through December.

### Fault Tolerance & Offline Fallback Strategy
If the NLR federal API experiences network latency, rate limiting, or server downtime, [`core/solar_engine.py`](./core/solar_engine.py) catches the exception and automatically switches to an empirical fallback calculation:
* Uses the **National Solar Radiation Database (NSRDB)** regional multi-year averages:
  * **Sunbelt ($< 34^\circ\text{ N}$):** $1,650\text{ kWh AC per kW DC installed per year}$
  * **Temperate / California ($34^\circ\text{--}40^\circ\text{ N}$):** $1,460\text{ kWh AC per kW DC installed per year}$
  * **Northern ($> 40^\circ\text{ N}$):** $1,320\text{ kWh AC per kW DC installed per year}$
* Applies regional bell-curve weights across all 12 calendar months.
* The frontend sets `is_live_api = False` so the user knows an empirical fallback was used, ensuring the application **never crashes during a live presentation**.

---

## 2. Satellite Basemap Service: Esri ArcGIS World Imagery

* **Provider:** Environmental Systems Research Institute (Esri)
* **Tile URL Template:** `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
* **HTTP Method:** `GET`
* **Implementation File:** [`app.py`](./app.py) via `folium.TileLayer`

### How It Works Under the Hood
1. The user selects a school campus. The application passes the school’s latitude and longitude to Folium with a zoom level of $z = 17$.
2. Folium (which runs Leaflet.js in the browser) uses the Web Mercator projection (EPSG:3857) to convert the GPS coordinates into an $(x, y)$ tile coordinate index for that zoom level.
3. The browser requests $256 \times 256$ pixel JPEG aerial photograph tiles directly from Esri’s global content delivery network (CDN).
4. Over top of these tiles, Folium renders our dynamic **semi-transparent solar canopy circle/polygon overlay** (`fill_color="#fbbf24"`, `fill_opacity=0.45`), showing exactly how much of the parking lot is shaded by solar panels.

---

## 3. Spatial Parking Lot Extraction: OpenStreetMap API

* **Provider:** OpenStreetMap Foundation
* **Direct Bounding Box Map Endpoint:** `https://api.openstreetmap.org/api/0.6/map?bbox={min_lon},{min_lat},{max_lon},{max_lat}`
* **Alternative Overpass Query Endpoint:** `https://overpass-api.de/api/interpreter`
* **Implementation File:** [`core/data_ingest.py`](./core/data_ingest.py)

### How It Works
1. For any school GPS coordinate, we calculate a 400-meter bounding box using spherical degree offsets:
   $$\Delta \text{lat} = \frac{400\text{ m}}{111,000\text{ m/degree}}$$
   $$\Delta \text{lon} = \frac{400\text{ m}}{111,000\text{ m/degree} \times \cos(\text{lat})}$$
2. The endpoint returns vector XML/JSON polygons tagged with `amenity=parking`.
3. We parse coordinate pairs into `shapely.geometry.Polygon` objects and load them into a `geopandas.GeoDataFrame`.
4. We reproject from angular degrees (EPSG:4326) into metric UTM coordinates (`estimate_utm_crs()`) to compute true ground surface area in square meters ($m^2$).
5. **Canopy Packing Density Factor:** We apply an empirical $65\%$ usable canopy factor ($\eta = 0.65$) to account for fire lanes, turning aisles, and lighting pole setbacks.
6. **Calibration:** For our curated campuses, these footprints were verified against completed solar canopy rollouts from the Cupertino Union School District (CUSD) and Fremont Union High School District (FUHSD).

---

## 4. Student Speaking Guide: How to Explain the APIs to Judges

Here are three simple, effective ways for Pranav to explain the API architecture depending on the judge’s technical background:

### Option A: The 20-Second Pitch (For General Judges)
> *"Under the hood, we don't guess the solar numbers. When you select a school or move the slider, our Python backend sends the campus GPS coordinates and canopy size live to the **U.S. Department of Energy's PVWatts v8 REST API**. The federal supercomputer simulates sun angles, local temperatures, and panel physics to send back the exact monthly kilowatt-hours. Then, our map pulls high-resolution satellite tiles from Esri's ArcGIS servers so you can see the actual parking lot from space."*

### Option B: The Technical Deep Dive (For Software Engineering / GIS Judges)
> *"Our software architecture connects three distinct services:  
> 1. **Solar Modeling:** We query the DOE / NLR PVWatts v8 endpoint (`developer.nlr.gov`) using HTTP GET with parameters for latitude, longitude, DC capacity, a 10-degree tilt, and a 14% derate factor. We parse the JSON payload for `ac_annual` and `ac_monthly`.  
> 2. **GIS & Reprojection:** We pull parking vectors from OpenStreetMap, reproject from WGS 84 degrees into local UTM Cartesian meters using GeoPandas, and apply a 65% packing factor.  
> 3. **Satellite Tile Layer:** We embed Folium and Leaflet.js to request Web Mercator tiles at zoom level 17 from Esri's ArcGIS World Imagery server.  
> 4. **Fault Tolerance:** If the federal API ever times out, our code catches the error and falls back to regional NSRDB solar harvest constants, ensuring zero crash risk."*

---

## 5. Judge Q&A on APIs: Common Questions & Winning Answers

### Q1: "Where do you get your solar irradiance data, and is it live?"
> **Answer:** *"It is a live HTTP GET request to the U.S. Department of Energy / National Laboratory of the Rockies (NLR) PVWatts v8 API. It uses the National Solar Radiation Database (NSRDB), which is a 4km by 4km satellite grid of actual measured solar irradiance across North America."*

### Q2: "What happens if your internet fails or the federal government API is slow during your demo?"
> **Answer:** *"I built defensive fault tolerance into `core/solar_engine.py`. The HTTP call has an 8-second timeout. If it times out or returns a non-200 code, the engine automatically falls back to empirical NSRDB regional constants (like 1,460 kWh/kW-yr for Northern California) and distributes generation across all 12 months using seasonal bell curves. The app never crashes."*

### Q3: "Why did you use developer.nlr.gov instead of developer.nrel.gov?"
> **Answer:** *"In May 2026, the Department of Energy reorganized NREL under the National Laboratory of the Rockies (NLR), and retired the old `developer.nrel.gov` domain. If you call the old NREL endpoint today it redirects or fails, so our codebase uses the active `developer.nlr.gov` federal endpoint."*

### Q4: "How does the map know where the parking lot is?"
> **Answer:** *"We use OpenStreetMap spatial vectors tagged `amenity=parking`. We convert those coordinates into polygons using Shapely, reproject to local UTM coordinates using GeoPandas to get exact ground square meters, and then render them over Esri ArcGIS satellite tiles at zoom level 17."*
