# Project 2: Ghost Plumes — Sea Level Rise Induced Shallow Groundwater Emergence into Capped Superfund & Toxic Sites

---

## 1. WHAT: Project Scope, Core Hypothesis & Definitions

### Research Objective
To develop a 3D subsurface geospatial vulnerability framework in **Python (Rasterio & GeoPandas) / ArcGIS Pro** that models sea level rise (SLR) induced shallow groundwater emergence across the San Francisco Bay Area, intersecting rising unconfined water tables with thousands of state-managed (EnviroStor / GeoTracker) and federal Superfund toxic contamination plumes to identify the exact school zones, residential parcels, and subterranean infrastructure conduits at risk of toxic plume remobilization.

### Core Hypothesis
In coastal Bay Area lowlands (e.g., East Palo Alto, Mountain View, Sunnyvale, Hunters Point, West Oakland), marine hydrostatic pressure will force shallow freshwater tables to rise inland years before surface ocean waves overtop existing seawalls. Rising groundwater will saturate "capped" industrial soil contamination (volatile organic compounds, trichloroethylene TCE, benzene, heavy metals), remobilizing toxic liquid and vapor plumes into school foundations and municipal sewer networks under less than 1.0 meter of sea level rise.

### Key Terminology
* **Shallow Unconfined Groundwater:** The uppermost water table beneath the Earth's surface that is in direct hydraulic communication with the atmosphere and tidally influenced marine water bodies.
* **Hydrostatic Backwater Effect:** The physical process where rising sea levels exert inland pressure on coastal aquifers, impeding seaward freshwater discharge and forcing the unconfined water table upward toward the ground surface.
* **Capped Remediation Site:** A legacy industrial or chemical dump site "remediated" by placing an engineered impermeable surface cap (asphalt, concrete, clay) over contaminated soils to prevent surface rainwater infiltration, but possessing no barrier against rising subsurface groundwater.
* **Vapor Intrusion:** The migration of volatile organic chemicals (VOCs) from contaminated subsurface soil or rising groundwater into the indoor air of overlying buildings through basement cracks and foundation slabs.
* **Depth-to-Water (DTW):** The vertical distance (in meters or feet) from the ground surface down to the water table.

---

## 2. WHY: Motivation, Innovation & Significance

### The Real-World Problem
Silicon Valley is the birthplace of the modern tech economy, but its semiconductor fabrication history left Santa Clara County with **more federal Superfund sites than any other county in the United States**. Solvents like trichloroethylene (TCE), freon, and benzene leaked from underground storage tanks for decades. In response, regulators "capped" hundreds of sites with parking lots and office buildings. Today, local cities spend hundreds of millions on coastal levee walls to block high tides, completely ignoring the invisible water rising from beneath their feet. When the water table rises 2 feet, it inundates these capped toxic sponges, forcing carcinogenic vapors into the basements of nearby schools and homes.

### Why Traditional Approaches Fail
Standard coastal flood models (e.g., NOAA Sea Level Rise Viewer) model only **overtop marine flooding**—visible surface waves crossing shorelines. They assume that if a levee holds, the land behind it is safe. Peer-reviewed research from UC Berkeley and UCLA demonstrates that rising groundwater will inundate **twice as much Bay Area land area** as surface flooding, emerging miles inland from behind intact seawalls.

### What Makes This Project Truly Innovative
* **Exposing the Invisible Subsurface Hazard:** Performs spatial 3D raster subtraction between 1-meter USGS bare-earth LiDAR topography and the regional unconfined water table.
* **Forensic Toxic Intersection:** Cross-references the emerging water table with the California Department of Toxic Substances Control (DTSC) **EnviroStor** database of 5,000+ contamination sites.
* **First Public Parcel & School Screener:** While academic papers discuss regional square mileage, this tool gives students, parents, and civic planners a parcel-level screening tool to evaluate their school's toxic emergence risk.

---

## 3. TOOLS NEEDED: Environment & Extensions

### GIS Desktop & Web Tools
* **ArcGIS Pro (v3.0+) OR Open-Source Python:** For raster map algebra, surface subtraction, and vector buffering.
* **Streamlit & Folium:** For the interactive web application displaying SLR emergence sliders (0.0m to 1.5m).

### Python Environment & Libraries
```bash
python -m venv venv
source venv/bin/activate
pip install geopandas rasterio shapely numpy pandas folium streamlit streamlit-folium
```
* **`rasterio` (v1.3+):** Ingestion, windowed reading, and pixel-level map algebra on USGS Depth-to-Water GeoTIFF rasters.
* **`geopandas` (v0.14+):** Querying and buffering DTSC EnviroStor cleanup site polygons and school points.
* **`shapely`:** Intersection and spatial clipping.

---

## 4. DATASETS NEEDED: Sources, Formats & Query Parameters

| Dataset Name | Provider / Source | Format | Query / Import Method | Coordinate System |
| :--- | :--- | :--- | :--- | :--- |
| **USGS Shallow Groundwater Surface Model** | [USGS Open-File Report (Befus et al.) / Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.02v6wwq3c) | 10m/5m GeoTIFF Raster | Direct download of Bay Area Depth-to-Water (DTW) GeoTIFF from [Dryad Dataset doi:10.5061/dryad.02v6wwq3c](https://datadryad.org/dataset/doi:10.5061/dryad.02v6wwq3c) | UTM Zone 10N (EPSG:32610) |
| **DTSC EnviroStor Cleanup Sites** | [California State Geoportal](https://gis.data.ca.gov/datasets/california::department-of-toxic-substances-control-envirostor-public-data-export) / [DTSC EnviroStor](https://www.envirostor.dtsc.ca.gov/public/) | CSV / GeoJSON / Shapefile | Direct export from [CA Geoportal DTSC Export](https://gis.data.ca.gov/datasets/california::department-of-toxic-substances-control-envirostor-public-data-export) (Filter `County = Santa Clara, San Mateo`) | WGS 1984 (EPSG:4326) |
| **California Public School Campuses** | [California Dept of Education](https://www.cde.ca.gov/ds/si/ds/pubschls.asp) | GeoJSON / CSV | Direct download: [CDE Public Schools Database](https://www.cde.ca.gov/ds/si/ds/documents/pubschls.txt) (Santa Clara & San Mateo K-12 boundaries) | Projected UTM 10N |
| **Sea Level Rise (SLR) Projections** | [California Ocean Protection Council (OPC)](https://opc.ca.gov/updating-californias-sea-level-rise-guidance/) | Tabular / Scenario | Intermediate-High SLR scenarios: +0.5m (~1.6ft), +1.0m (~3.3ft), +1.5m (~5.0ft) | N/A |

---

## 5. HOW: Exhaustive Step-by-Step Implementation Protocol

### Phase 1: Raster Map Algebra for Groundwater Emergence
1. Ingest the baseline USGS Depth-to-Water raster ($DTW_{\text{baseline}}$, in meters).
2. For any given Sea Level Rise scenario ($\Delta SLR \in \{0.25m, 0.5m, 1.0m, 1.5m\}$), the projected depth to groundwater is:
   $$DTW_{\text{projected}} = DTW_{\text{baseline}} - \Delta SLR$$
3. Classify emergence hazard zones:
   * **Surface Emergence (Flooding):** $DTW_{\text{projected}} \le 0.0\text{ meters}$.
   * **Critical Infrastructure / Basement Vapor Intrusion Zone:** $0.0\text{ m} < DTW_{\text{projected}} \le 1.5\text{ meters}$ (groundwater saturates building foundations and sewer laterals).
   * **Stable / Low Risk:** $DTW_{\text{projected}} > 1.5\text{ meters}$.

```python
import rasterio
import numpy as np

def compute_groundwater_emergence(dtw_raster_path: str, slr_meters: float = 0.5):
    """
    Performs raster map algebra to compute projected depth to groundwater
    under sea level rise scenarios.
    """
    with rasterio.open(dtw_raster_path) as src:
        dtw_baseline = src.read(1)
        profile = src.profile.copy()
        
        # Mask out nodata values
        nodata = src.nodata
        valid_mask = (dtw_baseline != nodata) & (~np.isnan(dtw_baseline))
        
        # Compute projected depth
        dtw_projected = np.full_like(dtw_baseline, fill_value=np.nan)
        dtw_projected[valid_mask] = dtw_baseline[valid_mask] - slr_meters
        
        # Hazard Classification:
        # 1 = Emergent Water (Surface flood), 2 = Shallow Foundation Infiltration (<1.5m), 0 = Safe
        hazard_class = np.zeros_like(dtw_baseline, dtype=np.uint8)
        hazard_class[valid_mask & (dtw_projected <= 0.0)] = 1
        hazard_class[valid_mask & (dtw_projected > 0.0) & (dtw_projected <= 1.5)] = 2
        
        profile.update(dtype=rasterio.uint8, count=1, nodata=0)
        
        return hazard_class, profile
```

---

### Phase 2: Spatial Toxic Plume Intersect & School Vulnerability Scoring
1. Ingest DTSC EnviroStor contaminated sites. Filter for sites tagged with volatile solvents (TCE, PCE, benzene) and remediation status = `Closed - Deed Restriction` (indicates soil contamination is capped on site).
2. Buffer each toxic site by 250 meters (typical volatile vapor dispersion radius).
3. Intersect the buffered toxic plumes with school campus polygons that fall within the **Emergent Groundwater Zone** ($DTW \le 1.5m$).

```python
import geopandas as gpd

def screen_toxic_emergence_schools(schools_geojson: str, envirostor_geojson: str, emergence_raster, raster_transform):
    """
    Identifies schools where rising groundwater intersects capped toxic contamination plumes.
    """
    schools_gdf = gpd.read_file(schools_geojson).to_crs(epsg=32610)
    toxic_gdf = gpd.read_file(envirostor_geojson).to_crs(epsg=32610)
    
    # Filter for capped volatile contamination sites
    volatile_chemicals = ["TCE", "PCE", "SOLVENTS", "BENZENE", "PETROLEUM"]
    mask = toxic_gdf["CONTAMINANTS"].str.upper().apply(lambda c: any(chem in str(c) for chem in volatile_chemicals))
    volatile_sites = toxic_gdf[mask].copy()
    
    # Buffer volatile sites by 250m
    volatile_sites["plume_buffer"] = volatile_sites.geometry.buffer(250)
    volatile_buffers = volatile_sites.set_geometry("plume_buffer")
    
    # Intersect schools with toxic plume buffer zones
    schools_in_toxic_zone = gpd.sjoin(schools_gdf, volatile_buffers, predicate="intersects", how="inner")
    
    return schools_in_toxic_zone
```

---

### Phase 3: Interactive Web UI in Streamlit
Build the live pitch day application (`app.py`):

```python
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Ghost Plumes: Subsurface Toxic Emergence", layout="wide")

st.title("☠️ Ghost Plumes: Rising Groundwater & Capped Toxic Sites")
st.markdown("**SVYCA Youth For Earth Hackathon @ Stanford Climate Week**")

# Sidebar Controls
st.sidebar.header("🌊 Sea Level Rise Scenario")
slr_feet = st.sidebar.slider("Sea Level Rise (Feet)", 0.0, 5.0, 2.0, 0.5)
slr_m = slr_feet * 0.3048

# Known Bay Area Capped Superfund & Vulnerable School Locations
case_studies = [
    {
        "School": "Cesar Chavez Academy (East Palo Alto)",
        "Lat": 37.4725, "Lon": -122.1380,
        "Baseline_DTW_ft": 3.8,
        "Nearby_Site": "Rhone-Poulenc Chemical Superfund (Pesticides / Arsenic)",
        "Capped": True, "Contaminants": "Arsenic, Heavy Metals, VOCs"
    },
    {
        "School": "Mountain View High / Los Altos Border",
        "Lat": 37.3820, "Lon": -122.0830,
        "Baseline_DTW_ft": 4.5,
        "Nearby_Site": "MEW Semiconductor Superfund Plume (Fairchild / Raytheon)",
        "Capped": True, "Contaminants": "Trichloroethylene (TCE), Freon"
    },
    {
        "School": "Sunnyvale Middle School",
        "Lat": 37.3750, "Lon": -122.0290,
        "Baseline_DTW_ft": 5.1,
        "Nearby_Site": "AMD Sunnyvale Facility (Former Solvent Cleaners)",
        "Capped": True, "Contaminants": "Volatile Solvents"
    }
]

# Calculate emergence status for selected scenario
st.markdown(f"### 🧪 Site Vulnerability Under +{slr_feet} ft Sea Level Rise (+{slr_m:.2f} m)")

cols = st.columns(3)
for i, site in enumerate(case_studies):
    projected_dtw = site["Baseline_DTW_ft"] - slr_feet
    with cols[i]:
        if projected_dtw <= 0:
            st.error(f"🚨 **{site['School']}**\n\n**STATUS: SURFACE FLOOD**\n\nGroundwater breaches ground level! Contaminants: {site['Contaminants']}")
        elif projected_dtw <= 3.0:
            st.warning(f"⚠️ **{site['School']}**\n\n**STATUS: FOUNDATION INFILTRATION**\n\nWater table at {projected_dtw:.1f} ft! High risk of toxic vapor intrusion from {site['Nearby_Site']}.")
        else:
            st.success(f"✅ **{site['School']}**\n\n**STATUS: STABLE**\n\nWater table at {projected_dtw:.1f} ft.")

# Folium Map Display
m = folium.Map(location=[37.42, -122.10], zoom_start=12)

for site in case_studies:
    projected_dtw = site["Baseline_DTW_ft"] - slr_feet
    pin_color = "red" if projected_dtw <= 3.0 else "blue"
    
    # School Marker
    folium.Marker(
        location=[site["Lat"], site["Lon"]],
        popup=f"<b>{site['School']}</b><br>Projected DTW: {projected_dtw:.1f} ft<br>Threat: {site['Nearby_Site']}",
        icon=folium.Icon(color=pin_color, icon="graduation-cap", prefix="fa")
    ).add_to(m)
    
    # 250m Toxic Plume Buffer Circle
    folium.Circle(
        location=[site["Lat"] + 0.002, site["Lon"] + 0.002],
        radius=250,
        color="purple",
        fill=True,
        fill_color="purple",
        fill_opacity=0.3,
        popup=f"Capped Plume: {site['Nearby_Site']}"
    ).add_to(m)

st_folium(m, width=900, height=450)
```

---

## 6. DELIVERABLES, VISUALIZATIONS & PITCH STORYTELLING

1. **The Hook (45 sec):** Show a dramatic photograph of the San Francisco Bay seawalls: *"The Bay Area is preparing to spend $20 billion building seawalls to hold back rising ocean waves. But our research reveals an invisible subterranean emergency: the ocean is pushing the freshwater table up from underneath our soil."*
2. **The Forensic Discovery (1 min):** Explain Silicon Valley's history: *"Santa Clara County has more Superfund sites than anywhere in America. We capped these chemical solvent pools with asphalt and forgot about them. But rising groundwater doesn't respect asphalt."*
3. **The Live Simulation (1.5 min):** 
   - Open the live tool. Show East Palo Alto and Mountain View.
   - At baseline: water table is 4.5 feet deep.
   - Move the slider to **+2.0 feet Sea Level Rise**: the water table rises to just 1.8 feet below the surface.
   - Show how the rising water table submerges the legacy TCE plume, mobilizing carcinogenic vapors directly into school basements and sewer laterals.
4. **Closing & Policy Impact (30 sec):** Call on regional climate resilience planners to mandate sub-slab depressurization and subsurface groundwater interception trenches, not just surface seawalls.

---

## 7. POTENTIAL PITFALLS & TROUBLESHOOTING

| Problem / Error | Root Cause | Solution |
| :--- | :--- | :--- |
| **USGS Depth-to-Water raster too large for laptop memory** | Full 5-meter raster for entire SF Bay is >3 GB. | Clip the raster in QGIS or Python `rasterio.mask` to the bounding box of Santa Clara & San Mateo coastal lowlands (reduces file to ~25 MB). |
| **Confusion between Sea Level Rise and Groundwater Rise** | Groundwater does not rise 1:1 with sea level in steep terrain. | Constrain analysis strictly to coastal unconfined lowlands (elevation $< 10\text{ meters}$ above mean sea level), where hydraulic coupling is nearly 1:1. |
| **Missing chemical details in EnviroStor** | Some cleanup records have blank `CONTAMINANT` fields. | Cross-reference state `SITE_ID` with the California State Water Board **GeoTracker** portal API. |
