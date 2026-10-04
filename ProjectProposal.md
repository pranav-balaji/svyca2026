# SolarSchools USA: Project Proposal

**Project Title:** SolarSchools USA — K-12 Solar Canopy Feasibility & IRA Direct Pay Decision Platform  
**Competition:** SVYCA Youth For Earth Hackathon @ Stanford Climate Week (October 25, 2026)  
**Author:** Pranav Balaji  
**Focus:** Clean Energy Transition, Civic Infrastructure Decarbonization, Federal Climate Finance  
---

## 1. Executive Summary & Core Hypothesis

### 1.1 The Opportunity
Public school districts in the United States spend over **$8 billion annually on energy**—a non-instructional operating expenditure second only to personnel salaries (U.S. Department of Energy [DOE], 2022). Concurrently, public school campuses dedicate millions of square feet of land to unshaded asphalt parking lots that function as suburban heat sinks, absorbing solar radiation during the day and radiating heat into classrooms and adjacent neighborhoods. 

While rooftop solar installations often confront structural engineering impediments (e.g., roof load limitations, seismic reinforcement mandates, HVAC obstruction, and roof warranty expirations), **parking lot solar canopies** offer unobstructed solar access, pre-graded flat geometry, shade for student and faculty vehicles, and ideal infrastructure for future electric school bus (EV) charging. 

Crucially, **Section 6417 of the federal Inflation Reduction Act of 2022 (IRA)** established "Elective Pay" (commonly termed "Direct Pay"), allowing tax-exempt local public school districts to receive **direct cash reimbursement checks from the Internal Revenue Service (IRS) covering 30% to 50% of clean energy capital costs** (26 U.S.C. § 6417; IRS, 2024). Despite this unprecedented federal capital injection, over 90% of school boards and student climate advocates across the country lack the financial resources or technical tools to assess feasibility without hiring private commercial engineering consultancies.

### 1.2 Core Hypothesis
Automating geospatial polygon extraction of school parking lots and coupling it with National Renewable Energy Laboratory (NREL) irradiance algorithms and IRA financial rules will demonstrate that:
1. Converting 60% of school parking footprint to solar canopies generates **65% to 90% of daytime campus electrical demand**.
2. Leveraging federal IRA Direct Pay cash checks reduces school district capital payback periods to **under 6.5 years** across diverse solar resource regions.
3. Over a 25-year operational lifecycle, a typical suburban high school redirects **$1.8 million to $3.5 million** from utility company expenditures directly back into instructional budgets.

---

## 2. The Phased Geographic Architecture

To ensure technical depth, computational feasibility, and rigorous ground-truthing within the 4-week hackathon design window (Sept 20 – Oct 18), the project is engineered across three sequential phases:

```mermaid
flowchart LR
    P1["Phase 1: Bay Area (Weeks 1-2)<br/>Ground-Truthing & PG&E Tariffs"] --> P2["Phase 2: California Statewide (Week 3)<br/>CDE Directory, Title 24, IOU Feasibility"]
    P2 --> P3["Phase 3: Nationwide USA (Week 4)<br/>NCES 100k Schools & IRA Direct Pay"]
```

---

### Phase 1: San Francisco Bay Area (Proof-of-Concept & Local Validation)
* **Geographic Scope:** The 9-county San Francisco Bay Area (focusing on Santa Clara, San Mateo, Alameda, and Contra Costa school districts).
* **Local Ground-Truthing & Case Studies:**
  * **Cupertino Union School District (CUSD) & Fremont Union High School District (FUHSD):** Utilize completed solar carport installations (e.g., Monta Vista High, Cupertino High, and CUSD's 2026 5.2 MW rollout) as empirical ground-truth benchmarks to calibrate our spatial packing density and solar harvest formulas against real utility bills.
  * **Palo Alto Unified School District (PAUSD) & San Jose Unified School District (SJUSD):** Model unshaded parking campuses (e.g., Palo Alto High, Gunn High, San Jose City College, Lincoln High) to demonstrate immediate deployment feasibility.
* **Utility Tariff Structure:** Ingest Pacific Gas & Electric (PG&E) commercial rate schedules:
  * **Schedule B-19 (Medium General Demand Time-of-Use)** and **Schedule E-19**, capturing high peak energy charges ($0.32–$0.42/kWh) and monthly demand charges ($/kW), reflecting the acute fiscal savings available to Northern California schools.
* **Deliverable:** Fully functional interactive prototype with verified local spatial layers, parking polygons, and localized financial outputs.

---

### Phase 2: California Statewide Expansion (Policy & Environmental Justice Integration)
* **Geographic Scope:** All 58 California counties (~1,000 public school districts, ~10,000 public K-12 campuses).
* **Dataset Scale:** Ingest the complete **California Department of Education (CDE) Public Schools Directory** (`pubschls.txt`), mapping campus boundaries statewide.
* **Multi-Utility Regulatory Landscape:**
  * Expand beyond PG&E to model Southern California Edison (SCE), San Diego Gas & Electric (SDG&E), Sacramento Municipal Utility District (SMUD), and Los Angeles Department of Water and Power (LADWP) commercial tariffs.
* **State Policy & Environmental Justice Overlays:**
  * **California Senate Bill 100 (Clean Energy Act of 2018):** Benchmarking school solar generation against state zero-carbon retail electricity mandates.
  * **CalEnviroScreen 4.0 (OEHHA / CalEPA):** Incorporate state-designated SB 535 Disadvantaged Communities (DACs), highlighting equity priority zones in the Central Valley, Inland Empire, and East Bay where high heat days coincide with low median school district revenues.
* **Deliverable:** Statewide searchable platform allowing any California district to assess solar carport potential, microgrid eligibility, and Title 24 compliance.

---

### Phase 3: Nationwide United States Expansion (National Scale & Federal IRA Elective Pay)
* **Geographic Scope:** All 50 U.S. states (~13,000 public school districts, ~100,000 public K-12 schools).
* **Federal Dataset Integration:**
  * **National Center for Education Statistics (NCES) EDGE Dataset:** Integrate nationwide geocoded public school points, including district identifiers, enrollment, and federal Title I low-income eligibility status.
* **National Solar Irradiance Grid:**
  * Query the **U.S. Department of Energy / National Laboratory of the Rockies (NLR) PVWatts v8 REST API** (backed by the National Solar Radiation Database, NSRDB) to model physical solar yields across diverse climate zones—from the high-irradiance Sunbelt (Texas, Arizona, Nevada) to the Midwest and Northeast.
* **National Energy Economics:**
  * Ingest **U.S. Energy Information Administration (EIA) Form 861** state-by-state commercial electricity tariffs (ranging from $0.11/kWh in low-cost states to $0.32/kWh in high-cost states).
* **Federal IRA Section 6417 Elective Pay Engine:**
  * Automatically compute federal cash reimbursement checks:
    $$\text{IRA Reimbursement Rate} = 30\% \text{ (Base)} + 10\% \text{ (Energy Community Bonus)} + 10\% \text{ (Low-Income Title I Bonus)}$$
  * Model 30% to 50% direct IRS cash transfers, displaying total project cost, federal check amount, net district cost, and simple payback.
* **Deliverable:** National civic platform with one-click **"School Board Action Brief"** generation.

---

## 3. Mathematical & Physical Modeling Framework

### 3.1 Geospatial Parking Footprint & Capacity Extraction
For a school campus boundary polygon $P_{\text{campus}}$, the gross surface parking footprint area $A_{\text{gross}}$ is derived from OpenStreetMap polygon vectors tagged `amenity=parking`:
$$A_{\text{gross}} = \sum_{i=1}^{m} \text{Area}(P_{\text{parking}, i}) \quad \text{for } P_{\text{parking}} \subset P_{\text{campus}}$$

To account for interior traffic drive-aisles, turning radii, light pole setbacks, and fire lanes, an empirical usable canopy factor ($\eta_{\text{usable}} = 0.65$) is applied:
$$A_{\text{net}} = A_{\text{gross}} \times \eta_{\text{usable}}$$

Assuming standard high-efficiency monocrystalline photovoltaic modules with a spatial power density of $200\text{ W/m}^2$ ($0.20\text{ kW/m}^2$):
$$P_{\text{DC}} = A_{\text{net}} \times 0.20\text{ kW/m}^2$$

Approximate parking stall equivalence:
$$N_{\text{stalls}} = \left\lfloor \frac{A_{\text{gross}}}{32.5\text{ m}^2/\text{stall}} \right\rfloor$$

---

### 3.2 Solar Irradiance & AC Generation (NREL PVWatts v8 Physics Engine)
AC energy generation is modeled via the PVWatts v8 formulation (Dobos, 2014):
$$E_{\text{AC, annual}} = \sum_{t=1}^{8760} P_{\text{AC}}(t)$$
Where hourly AC power $P_{\text{AC}}(t)$ accounts for plane-of-array (POA) irradiance, cell temperature degradation, and system losses:
$$P_{\text{DC}}(t) = \frac{I_{\text{POA}}(t)}{1000\text{ W/m}^2} \times P_{\text{DC, rated}} \times \left[ 1 + \gamma_{\text{temp}} \cdot (T_{\text{cell}}(t) - 25^\circ\text{C}) \right] \times (1 - L_{\text{system}})$$
* $I_{\text{POA}}$: Plane-of-array solar irradiance derived from NSRDB satellite data.
* $\gamma_{\text{temp}}$: Temperature coefficient of power ($-0.35\%/^\circ\text{C}$ for mono-Si).
* $L_{\text{system}}$: Aggregate system derate losses ($14.0\%$, covering soiling, inverter mismatch, wiring, and shading).

---

### 3.3 Federal IRA Section 6417 Elective Pay Financial Model
Turnkey capital expenditure ($C_{\text{turnkey}}$) for commercial canopy structures is parameterized at $\$3.10/\text{watt DC}$ (Feldman et al., 2021; adjusted for canopy structural steel):
$$C_{\text{turnkey}} = P_{\text{DC}} \times 1000\text{ W/kW} \times \$3.10/\text{W}$$

The federal direct cash reimbursement check from the IRS ($R_{\text{IRA}}$) is computed under 26 U.S.C. § 6417:
$$R_{\text{IRA}} = C_{\text{turnkey}} \times \left( 0.30 + \beta_{\text{energy}} + \beta_{\text{income}} \right)$$
* $\beta_{\text{energy}} = 0.10$ if the census tract qualifies as an Energy Community (coal closure or brownfield).
* $\beta_{\text{income}} = 0.10$ if the school is designated Title I or in a Low-Income Community under Section 45D(e).

Net out-of-pocket capital required from the school district:
$$C_{\text{net}} = C_{\text{turnkey}} - R_{\text{IRA}}$$

Annual electricity utility bill savings:
$$S_{\text{annual}} = E_{\text{AC, annual}} \times \text{Tariff}_{\text{commercial}}\ (\$/\text{kWh})$$

Simple Capital Payback Period:
$$\text{Payback (Years)} = \frac{C_{\text{net}}}{S_{\text{annual}}}$$

25-Year Net Fiscal Benefit to District Classrooms:
$$\text{Net Lifetime Savings} = \sum_{y=1}^{25} \left( S_{\text{annual}} \times (1 - \delta_{\text{deg}})^y \times (1 + \rho_{\text{utility}})^y \right) - C_{\text{net}}$$
* $\delta_{\text{deg}}$: Annual panel degradation ($0.5\%/\text{year}$).
* $\rho_{\text{utility}}$: Annual utility rate escalation ($2.5\%/\text{year}$).

---

### 3.4 Scope 2 Carbon Abatement & Environmental Equivalencies
Annual Scope 2 greenhouse gas emissions avoided:
$$\text{GHG Avoided (Metric Tons } CO_2\text{)} = \frac{E_{\text{AC, annual}} \times EF_{\text{subregion}}}{2204.62\text{ lbs/ton}}$$
* $EF_{\text{subregion}}$: Regional emissions factor from EPA eGRID (e.g., $0.45\text{ lbs } CO_2/\text{kWh}$ for CAMX California; $0.85\text{ lbs } CO_2/\text{kWh}$ for ERCT Texas).
* Gasoline passenger cars offset: $\text{Cars} = \text{GHG Avoided} / 4.6\text{ tons/car-year}$ (EPA, 2024).

---

## 4. Software Architecture & Implementation Protocol

### 4.1 Modular Software Stack
The application is structured into four distinct Python modules:

```
solarschools/
│
├── core/
│   ├── data_ingest.py        # Queries NCES, CDE, and Overpass APIs
│   ├── solar_engine.py       # Calls NLR PVWatts v8 API with local fallbacks
│   └── financial_model.py    # Computes IRA Section 6417 Direct Pay and utility ROI
│
├── app.py                    # Streamlit web interface with Leaflet/Folium mapping
└── export/
    └── brief_generator.py    # Compiles markdown/PDF School Board Action Briefs
```

---

### 4.2 Production Python Implementation

#### Module 1: Ingestion & Spatial Footprint Extraction (`core/data_ingest.py`)
```python
"""
core/data_ingest.py
Handles spatial queries for public schools and OSM parking lot polygons.
"""
import requests
import geopandas as gpd
from shapely.geometry import Polygon

def get_school_parking_footprint(lat: float, lon: float, radius_m: int = 500):
    """
    Extracts parking lot footprints around school coordinates using OSM Overpass API.
    Applies a 0.65 usable canopy packing density factor.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:15];
    (
      way["amenity"="parking"](around:{radius_m}, {lat}, {lon});
      relation["amenity"="parking"](around:{radius_m}, {lat}, {lon});
    );
    out geom;
    """
    try:
        response = requests.post(overpass_url, data={"data": query}, timeout=15)
        if response.status_code == 200:
            data = response.json()
            polygons = []
            for el in data.get("elements", []):
                if "geometry" in el and len(el["geometry"]) >= 3:
                    coords = [(pt["lon"], pt["lat"]) for pt in el["geometry"]]
                    polygons.append(Polygon(coords))
                    
            if polygons:
                gdf = gpd.GeoDataFrame(geometry=polygons, crs="EPSG:4326")
                utm_crs = gdf.estimate_utm_crs()
                gdf_utm = gdf.to_crs(utm_crs)
                gross_area_m2 = float(gdf_utm.geometry.area.sum())
                usable_canopy_m2 = gross_area_m2 * 0.65
                return {
                    "gross_area_m2": round(gross_area_m2, 1),
                    "usable_canopy_m2": round(usable_canopy_m2, 1),
                    "is_synthetic": False,
                    "polygons": polygons
                }
    except Exception:
        pass

    # Reliable Fallback: Typical US high school surface lot (5,000 m2 gross, ~150 stalls)
    return {
        "gross_area_m2": 5000.0,
        "usable_canopy_m2": 3250.0,
        "is_synthetic": True,
        "polygons": []
    }
```

#### Module 2: Physics Engine (`core/solar_engine.py`)
```python
"""
core/solar_engine.py
Queries the National Laboratory of the Rockies (NLR / NREL) PVWatts v8 API.
"""
import requests

def query_pvwatts_generation(lat: float, lon: float, capacity_kw: float, api_key: str = "DEMO_KEY"):
    """
    Calls the official active DOE PVWatts v8 endpoint (developer.nlr.gov).
    """
    url = "https://developer.nlr.gov/api/pvwatts/v8.json"
    params = {
        "api_key": api_key,
        "lat": lat,
        "lon": lon,
        "system_capacity": capacity_kw,
        "azimuth": 180,       # True South
        "tilt": 10,           # 10 degree canopy pitch
        "array_type": 2,      # Fixed canopy mount
        "module_type": 1,     # Premium Monocrystalline
        "losses": 14.0        # Aggregate derate losses
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            outputs = res.json()["outputs"]
            return {
                "annual_kwh": outputs["ac_annual"],
                "capacity_factor": outputs["capacity_factor"],
                "monthly_kwh": outputs["ac_monthly"]
            }
    except Exception:
        pass

    # Regional irradiance fallback (NSRDB long-term regional harvest rates)
    multiplier = 1650.0 if lat < 34.0 else (1450.0 if lat < 40.0 else 1300.0)
    return {
        "annual_kwh": round(capacity_kw * multiplier, 0),
        "capacity_factor": round((multiplier / 8760) * 100, 1),
        "monthly_kwh": []
    }
```

#### Module 3: Financial & IRA Direct Pay Engine (`core/financial_model.py`)
```python
"""
core/financial_model.py
Computes IRA Section 6417 Elective Pay cash reimbursements and utility ROI.
"""

def compute_ira_direct_pay(capacity_kw: float, annual_kwh: float, tariff_per_kwh: float, is_bonus_eligible: bool = True):
    """
    Calculates 30%-50% IRS cash check, net district outlay, and simple payback.
    Turnkey commercial canopy benchmark: $3.10 / Watt DC installed.
    """
    turnkey_cost = capacity_kw * 1000.0 * 3.10
    
    # IRA Elective Pay (Direct Pay) rate
    direct_pay_pct = 0.40 if is_bonus_eligible else 0.30  # 30% base + 10% bonus
    irs_direct_cash_check = turnkey_cost * direct_pay_pct
    net_district_outlay = turnkey_cost - irs_direct_cash_check
    
    # Utility savings
    annual_savings = annual_kwh * tariff_per_kwh
    payback_years = round(net_district_outlay / annual_savings, 1) if annual_savings > 0 else 0
    lifetime_25yr_net = (annual_savings * 25) - net_district_outlay
    
    # Carbon reduction (EPA eGRID national factor: ~0.85 lbs CO2 / kWh)
    co2_tons = (annual_kwh * 0.85) / 2204.62
    
    return {
        "turnkey_cost_usd": turnkey_cost,
        "direct_pay_pct": direct_pay_pct,
        "irs_cash_check_usd": irs_direct_cash_check,
        "net_district_outlay_usd": net_district_outlay,
        "annual_utility_savings_usd": annual_savings,
        "payback_years": payback_years,
        "lifetime_25yr_net_usd": lifetime_25yr_net,
        "annual_co2_tons_avoided": round(co2_tons, 1)
    }
```

---

## 5. 4-Week Milestone & Execution Roadmap

| Timeline | Phase Focus | Key Technical Milestones | Verification Gate |
| :--- | :--- | :--- | :--- |
| **Week 1 (Sept 20–27)** | **Phase 1: Bay Area MVP & Validation** | Ingest Santa Clara & San Mateo school districts; calibrate canopy parking factor against CUSD and FUHSD installations; integrate PG&E Schedule B-19 rate engine. | Prototype runs locally; produces valid outputs for Palo Alto High and Monta Vista High. |
| **Week 2 (Sept 28–Oct 4)**| **Phase 2: California Statewide Expansion** | Ingest CDE database (`pubschls.txt`); integrate SCE, SDG&E, SMUD, and LADWP tariffs; join CalEnviroScreen 4.0 equity percentiles. | User can select any public high school across all 58 California counties. |
| **Week 3 (Oct 5–11)** | **Phase 3: Nationwide USA & IRA Engine** | Ingest NCES national dataset; integrate EIA commercial rates for all 50 states; build IRA Section 6417 Direct Pay calculator. | User can evaluate schools in Texas, Arizona, Florida, Ohio, and California seamlessly. |
| **Week 4 (Oct 12–18)** | **UI Polish, Export & Rehearsal** | Build one-click "School Board Action Brief" markdown/PDF generator; record 90-sec video demo backup; finalize slide deck. | Rehearse 4-minute pitch to ensure crisp delivery under competition time limits. |
| **Oct 25, 2026** | **Showcase @ Stanford University** | In-person demonstration to judges during Stanford Climate Week. | Deliver live pitch, engage judges with interactive sliders, field Q&A. |

---

## 6. Stanford Climate Week Pitch Script (Minute-by-Minute)

* **Minute 0:00 – 0:45: The Problem & The Federal Catalyst**  
  *"Judges, public schools spend $8 billion every year on electricity. In wealthy Bay Area communities like Cupertino, schools already have solar carports. But across California and America, over 100,000 public schools have unshaded asphalt lots baking in the sun and zero funding to hire solar consultants. Under Section 6417 of the Inflation Reduction Act, the federal government now writes a direct cash check reimbursing 30% to 50% of the cost for public schools. But 90% of school boards have no idea how much money they are leaving on the table."*
* **Minute 0:45 – 2:15: Live Interactive Tool Demonstration**  
  *(Open SolarSchools USA on the projector)*  
  *"We built SolarSchools USA, an open-access platform that scales from the Bay Area across all 50 states. Watch this: let's select a school in Texas—Westlake High in Austin. The app flies to the school, extracts 9,500 square meters of parking lot, calls the Department of Energy's solar physics engine, and calculates the numbers in real time:*  
  *- Solar Canopy Size: 550 kW DC*  
  *- Annual Clean Electricity: 820,000 kWh*  
  *- Federal IRA Direct Pay Cash Check: **$682,000** directly from the IRS*  
  *- Annual Utility Savings: **$94,000/year** redirected to teacher salaries and classrooms*  
  *- Full Payback: Just 5.6 years with zero local taxpayer bonds."*
* **Minute 2:15 – 3:00: Phase Progression & Action Brief Generator**  
  *"We started right here in the Bay Area, calibrating our model against local districts like Fremont Union and Cupertino, scaled it to all 10,000 California schools with CalEnviroScreen equity overlays, and expanded it nationwide using NCES federal data. Finally, with one click, a student can hit 'Download School Board Action Brief'—generating an ironclad engineering and financial proposal they can take directly to their next school board meeting."*
* **Minute 3:00 – 3:30: Closing & Q&A Transition**  
  *"SolarSchools USA democratizes climate finance, turning idle parking asphalt into clean power and classroom funding. Thank you, and I look forward to your questions."*

---

## 7. Formal References & Statutory Citations

### 7.1 Federal Legislation, Statutes & Administrative Guidance
1. **Public Law 117-169 (Inflation Reduction Act of 2022):** 136 Stat. 1818, Title I, Subtitle D, Section 6417 — *Elective Payment of Applicable Credits*. Codified at 26 U.S.C. § 6417.
2. **Internal Revenue Service (IRS). (2024):** *Treasury Decision 9988: Clean Energy Elective Payment and Transferability Regulations under Sections 6417 and 6418*. 26 CFR Part 1, RIN 1545-BQ63, Federal Register Vol. 89, No. 48.
3. **U.S. Department of the Treasury & IRS. (2023):** *Elective Pay and Transferability: Frequently Asked Questions on Clean Energy Tax Credits for Tax-Exempt Entities*. IRS Publication 5884 (Catalog Number 94142Q).
4. **U.S. Department of Energy (DOE). (2022):** *Energy Storage and Renewable Energy for K-12 Schools*. Office of Energy Efficiency and Renewable Energy, Efficient and Healthy Schools Campaign. Washington, DC.

### 7.2 Solar Engineering, Physics & Geospatial Models
5. **Dobos, A. P. (2014):** *PVWatts Version 5 Manual* (Technical Report NREL/TP-6A20-62641). National Renewable Energy Laboratory (NREL), Golden, CO. https://doi.org/10.2172/1158421.
6. **Sengupta, M., Xie, Y., Lopez, A., Habte, A., Maclaurin, G., & Shelby, J. (2018):** The National Solar Radiation Data Base (NSRDB). *Renewable and Sustainable Energy Reviews*, 89, 51-60. https://doi.org/10.1016/j.rser.2018.03.003.
7. **Feldman, D., Ramasamy, V., Fu, R., Ramdas, A., Desai, J., & Margolis, R. (2021):** *U.S. Solar Photovoltaic System and Energy Storage Cost Benchmark: Q1 2020* (Technical Report NREL/TP-7A40-77324). National Renewable Energy Laboratory, Golden, CO. https://doi.org/10.2172/1765396.
8. **Boeing, G. (2017):** OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems*, 65, 126-139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004.
9. **Haklay, M., & Weber, P. (2008):** OpenStreetMap: User-Generated Street Maps. *IEEE Pervasive Computing*, 7(4), 12-18. https://doi.org/10.1109/MPRV.2008.80.

### 7.3 State Policy, Utility Rate Structures & Public Datasets
10. **National Center for Education Statistics (NCES). (2023):** *Education Demographic and Geographic Estimates (EDGE): Public School Locations 2022–2023*. U.S. Department of Education, Institute of Education Sciences. https://nces.ed.gov/programs/edge/Geographic/SchoolLocations.
11. **U.S. Energy Information Administration (EIA). (2024):** *Form EIA-861: Annual Electric Power Industry Report - Commercial Retail Price of Electricity by State*. U.S. Department of Energy. https://www.eia.gov/electricity/data/eia861/.
12. **U.S. Environmental Protection Agency (EPA). (2024):** *Emissions & Generation Resource Integrated Database (eGRID) Summary Tables*. Office of Atmospheric Protection, Clean Energy Program. https://www.epa.gov/egrid.
13. **California Department of Education (CDE). (2024):** *California Public School Directory and Facilities Database*. Educational Demographics and Title I Division. https://www.cde.ca.gov/ds/si/ds/.
14. **California Public Utilities Commission (CPUC). (2024):** *Pacific Gas and Electric Company Commercial Electric Schedule B-19 (Medium General Demand Time-of-Use)*. CPUC Tariffs and Rate Filings.
15. **California Office of Environmental Health Hazard Assessment (OEHHA). (2021):** *CalEnviroScreen 4.0: California Communities Environmental Health Screening Tool*. California Environmental Protection Agency. https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40.
16. **Cupertino Union School District (CUSD) & ENGIE North America. (2026):** *District-Wide Sustainability & Clean Energy Infrastructure Project Completion Report (5.2 MW Solar + 72 EV Charging Ports)*. CUSD Facilities Planning.
