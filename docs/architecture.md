# System Architecture & Technical Specifications

SolarSchools USA is an open-access geospatial decision platform that screens K-12 public school parking lots for solar canopy feasibility, utility bill savings, and federal Inflation Reduction Act (IRA) Direct Pay cash reimbursements.

---

## 1. High-Level System Architecture

```mermaid
flowchart TD
    subgraph UI ["User Interface (Streamlit)"]
        A["Campus Selector & Geographic Filters"] --> B["Interactive Parameter Controls<br/>(Coverage %, EV Chargers, Tariff $/kWh)"]
        B --> C["Folium Satellite Map<br/>& Plotly Visualizations"]
        B --> D["School Board Action Brief (Markdown)"]
    end

    subgraph Data ["Data Ingestion Layer (core/data_ingest.py)"]
        E["Public School Directory<br/>(NCES / CDE Database)"]
        F["OpenStreetMap Geospatial Extraction<br/>(Paved Parking Footprints)"]
    end

    subgraph Engine ["Computational Engine"]
        G["Solar Physics Engine (core/solar_engine.py)<br/>NLR / NREL PVWatts v8 REST API"]
        H["Financial & IRA Engine (core/financial_model.py)<br/>IRC Section 6417 Elective Pay & 25-Year LCOE"]
    end

    E --> UI
    F --> Engine
    G --> UI
    H --> UI
```

---

## 2. Core Computational Modules

### 2.1 Spatial Footprint Engine (`core/data_ingest.py`)
Calculates the net usable solar collector area from gross parking lot polygons:

$$A_{\text{usable}} = A_{\text{gross}} \times \left(\frac{C_{\text{user}}}{100}\right) \times \eta_{\text{packing}}$$

Where:
* $A_{\text{gross}}$: Total paved parking lot area ($m^2$) extracted from OpenStreetMap.
* $C_{\text{user}}$: User-selected lot coverage percentage (default: 65%).
* $\eta_{\text{packing}} = 0.65$: Empirical parking packing factor preserving 24-foot driving aisles, ADA handicap access routes, and 14-foot vertical clearance for yellow school buses (California Fire Code Title 24).

System direct current (DC) capacity is derived assuming commercial tier-1 monocrystalline panels:

$$P_{\text{DC}} = A_{\text{usable}} \times 0.200 \text{ kW/m}^2$$

---

### 2.2 Solar Physics Engine (`core/solar_engine.py`)
Queries the U.S. Department of Energy / National Laboratory of the Rockies (NLR) PVWatts v8 REST API (`https://developer.nlr.gov/api/pvwatts/v8.json`) for hourly and monthly AC kilowatt-hour generation:

$$\text{Annual Energy Output (kWh)} = P_{\text{DC}} \times \text{GHI} \times \eta_{\text{system}} \times \prod (1 - L_i)$$

Where:
* Fixed tilt angle: $10^\circ$ (standard carport canopy drainage slope).
* Azimuth: $180^\circ$ (true South).
* System losses $\sum L_i = 14.08\%$ (inverter conversion efficiency, thermal coefficient, soiling, wiring, and transformer losses).
* **Fault Tolerance:** If external network latency exceeds 8 seconds or rate limits are reached, the module automatically falls back to regional solar radiation constants from the National Solar Radiation Database (NSRDB): 1,650 kWh/kW-yr for Sunbelt, 1,460 kWh/kW-yr for Temperate, and 1,320 kWh/kW-yr for Northern latitudes.

---

### 2.3 Financial & Direct Pay Engine (`core/financial_model.py`)
Models upfront turnkey EPC capital expenditures, federal tax-credit reimbursement checks, and 25-year lifecycle cashflows:

#### Capital Expenditure (CapEx)
$$\text{CapEx}_{\text{total}} = (P_{\text{DC}} \times C_{\text{watt}} \times 1000) + (N_{\text{EV}} \times C_{\text{EV}})$$

Where:
* $C_{\text{watt}} = \$3.10/\text{W}$ (commercial steel canopy benchmark).
* $C_{\text{EV}} = \$6,000$ per dual-port Level 2 commercial EV charging station.

#### Federal IRA Section 6417 Elective Pay ("Direct Pay")
Under the Inflation Reduction Act of 2022 (26 U.S.C. § 6417), tax-exempt public school districts receive direct cash refunds from the U.S. Treasury:

$$R_{\text{IRA}} = \text{Base Rate } (30\%) + \text{Domestic Steel Bonus } (10\%) + \text{Title I Low-Income / Energy Community Bonus } (10\%)$$

$$\text{IRS Cash Check} = \text{CapEx}_{\text{total}} \times R_{\text{IRA}}$$

$$\text{Net District Outlay} = \text{CapEx}_{\text{total}} - \text{IRS Cash Check}$$

#### 25-Year Lifecycle Pro Forma
* **First-Year Savings:** $S_1 = E_{\text{annual}} \times T_{\text{utility}}$
* **Utility Tariff Escalation:** 2.5% per year ($e = 0.025$).
* **Panel Degradation:** 0.5% annual efficiency loss ($d = 0.005$).
* **Operations & Maintenance:** $\$15.00/\text{kW-yr}$ escalating at 2.0% annual inflation.

$$\text{Net Savings (Year } t) = \left[ E_{\text{annual}} (1 - d)^{t-1} \times T_{\text{utility}} (1 + e)^{t-1} \right] - \text{O&M}_t$$

---

## 3. Real-World Ground Truth Validation

The simulation model was calibrated against operational solar carport installations in Silicon Valley:

* **Benchmark Campus:** Monta Vista High School (Fremont Union High School District, Cupertino, CA).
* **Installed System:** 550 kW solar carports across student and staff lots (built with ENGIE Services).
* **Published District Utility Savings:** $\$139,200/\text{year}$.
* **SolarSchools USA Modeled Output:** $\$145,000/\text{year}$.
* **Empirical Match:** Within **4.17%** of published district utility records.
