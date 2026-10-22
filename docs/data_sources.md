# Data Sources & Methodology

SolarSchools USA relies exclusively on publicly accessible, government-maintained, or open-source datasets.

---

## 1. Primary Datasets

| Dataset | Provider / Source | Description | Access Method / URL |
| :--- | :--- | :--- | :--- |
| **Public School Directory** | National Center for Education Statistics (NCES) | National database of ~100,000 public primary and secondary schools. Includes GPS coordinates, student enrollment, and Title I eligibility. | [NCES EDGE School Locations](https://nces.ed.gov/programs/edge/Geographic/SchoolLocations) |
| **California School Directory** | California Department of Education (CDE) | Directory of public schools across California's 58 counties. Sourced via `pubschls.txt`. | [CDE Public Schools Database](https://www.cde.ca.gov/ds/si/ds/documents/pubschls.txt) |
| **Solar Irradiance (PVWatts v8)** | National Laboratory of the Rockies / U.S. DOE | REST API querying solar radiation data from the National Solar Radiation Database (NSRDB). | [NLR Developer Portal](https://developer.nlr.gov/) |
| **Parking Footprints** | OpenStreetMap (OSM) / Overpass API | Geospatial vector polygons defining parking lots (`amenity=parking`). | [OpenStreetMap API](https://api.openstreetmap.org/) |
| **Commercial Electricity Rates** | U.S. Energy Information Administration (EIA) | Average retail commercial electricity prices by state ($/kWh). | [EIA Form 861 Retail Sales Table 5a](https://www.eia.gov/electricity/sales_revenue/xls/table5_a.xlsx) |
| **Grid Carbon Factors** | U.S. Environmental Protection Agency (EPA) | Subregional greenhouse gas emission rates (lbs CO2/kWh) from the eGRID database. | [EPA eGRID Explorer](https://www.epa.gov/egrid/data-explorer) |
| **Energy Communities** | U.S. Department of Energy | Census tracts meeting coal closure, brownfield, or high-fossil-fuel employment criteria for +10% IRA bonus. | [DOE Energy Communities Mapping Tool](https://energycommunities.gov/energy-community-tax-incentive/) |

---

## 2. Geocoding & Coordinate Standard

All school coordinates in SolarSchools USA are strictly ground-truthed to the **paved surface of vehicular parking lots**, rather than the school's administrative building centroid. 

* **CRS:** WGS 84 (`EPSG:4326`) in decimal degrees.
* **Accuracy:** Calibrated to within 5 meters of main campus student/staff parking stalls using satellite imagery verification.
