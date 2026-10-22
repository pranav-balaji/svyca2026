# SolarSchools USA
# Copyright (c) 2026 Pranav Balaji
# SPDX-License-Identifier: Apache-2.0
"""
core/report_generator.py
Generates an executive-ready 1-Page School Board Action Brief summarizing
engineering feasibility, IRA Section 6417 cash checks, and lifecycle utility savings.
"""
from datetime import datetime
from typing import Dict, Any


def generate_action_brief_markdown(
    school_name: str,
    school_info: Dict[str, Any],
    footprint: Dict[str, Any],
    solar_metrics: Dict[str, Any],
    fin_metrics: Dict[str, Any],
    coverage_pct: int,
    num_ev_chargers: int
) -> str:
    """
    Constructs a comprehensive, professionally formatted Markdown Action Brief
    tailored for presentation to a School Board of Education.
    """
    today_str = datetime.now().strftime("%B %d, %Y")
    district = school_info.get("district", "Local School District")
    county = school_info.get("county", "Local")
    state = school_info.get("state", "CA")
    utility = school_info.get("utility", "Electric Utility")
    phase = school_info.get("phase", "SolarSchools USA")
    enrollment = school_info.get("enrollment", "N/A")

    usable_canopy_m2 = footprint.get("usable_canopy_m2", 0.0)
    system_kw = round(usable_canopy_m2 * 0.20, 1)
    annual_kwh = solar_metrics.get("annual_kwh", 0.0)
    cap_factor = solar_metrics.get("capacity_factor", 0.0)

    total_cost = fin_metrics.get("total_project_cost", 0.0)
    ira_pct = int(fin_metrics.get("ira_rebate_pct", 0.30) * 100)
    irs_check = fin_metrics.get("irs_direct_cash_check", 0.0)
    net_cost = fin_metrics.get("net_district_investment", 0.0)
    annual_savings = fin_metrics.get("annual_utility_savings", 0.0)
    payback_years = fin_metrics.get("payback_years", 0.0)
    lifetime_dividend = fin_metrics.get("lifetime_25yr_net_dividend", 0.0)
    co2_tons = fin_metrics.get("annual_co2_tons_avoided", 0.0)
    cars_offset = fin_metrics.get("passenger_cars_offset", 0.0)

    solar_status = school_info.get("solar_status", "Unshaded (Losing Money)")
    installed_yr = school_info.get("installed_year")
    deployment_details = school_info.get("deployment_details", "")

    if "Implemented" in solar_status:
        status_narrative = f"""
> **BENCHMARK LEADER STATUS:** This campus deployed solar canopies in {installed_yr}. 
> **Real-World Validation:** {deployment_details}
> Actively validates our engineering and financial models by saving approximately **${annual_savings:,.2f} per year** in avoided utility expenses.
"""
    else:
        inaction_3yr = annual_savings * 3
        inaction_5yr = annual_savings * 5
        status_narrative = f"""
> **OPPORTUNITY STATUS — THE COST OF INACTION:** This campus currently has unshaded asphalt baking in the sun.
> **Current Fiscal Drain:** {deployment_details}
> * **1-Year Inaction Cost:** ${annual_savings:,.2f} surrendered to the utility company.
> * **3-Year Delay Penalty:** ${inaction_3yr:,.2f} in forfeited classroom capital.
> * **5-Year Delay Penalty:** ${inaction_5yr:,.2f} lost forever to electricity bills.
> * **Unclaimed Federal Cash:** An upfront **${irs_check:,.2f} IRS Direct Pay check** is waiting at the U.S. Treasury.
"""

    md = f"""# School Board Action Brief: Clean Energy & IRA Direct Pay Plan
### **{school_name}**
**Governing Body:** Board of Education, {district}  
**Campus Grade Level:** {school_info.get('level', 'School')} | **Solar Status:** {solar_status}  
**Jurisdiction:** {county} County, {state} | **Retail Electric Provider:** {utility}  
**Date of Assessment:** {today_str} | **Project Phase:** {phase}  

---

## 1. Executive Summary & Recommended Action
This feasibility brief evaluates deploying solar photovoltaic carports over campus surface parking and blacktop areas at **{school_name}** (Enrollment: {enrollment:,} students). 

By capitalizing on **Section 6417 of the federal Inflation Reduction Act (IRA) of 2022 ("Elective Pay" / "Direct Pay")**, the district can claim an upfront cash reimbursement check of **${irs_check:,.2f} ({ira_pct}% of total capital expenditure)** directly from the U.S. Department of the Treasury without issuing local municipal bonds or raising property taxes.

{status_narrative}

* **Turnkey Project Capital Outlay:** ${total_cost:,.2f}
* **U.S. Treasury IRA Direct Pay Cash Check:** **${irs_check:,.2f}**
* **Net District Out-of-Pocket Investment:** **${net_cost:,.2f}**
* **Immediate Annual Utility Bill Savings:** **${annual_savings:,.2f} / year**
* **Simple Capital Payback Period:** **{payback_years} Years**
* **25-Year Cumulative Net Dividend to Classrooms:** **${lifetime_dividend:,.2f}**

---

## 2. Engineering & Geospatial Specifications
* **Gross Campus Parking Footprint:** {footprint.get('gross_area_m2', 0):,.0f} m² (~{footprint.get('parking_stalls', 0)} parking stalls)
* **Modeled Canopy Coverage:** {coverage_pct}% of available parking area
* **Net Active PV Canopy Area:** {usable_canopy_m2:,.0f} m² ({usable_canopy_m2 * 10.7639:,.0f} sq. ft.)
* **Nameplate DC System Capacity:** **{system_kw:,.1f} kW DC** (High-efficiency mono-Si modules, 200 W/m²)
* **First-Year AC Generation (PVWatts v8):** **{annual_kwh:,.0f} kWh / year** (Capacity Factor: {cap_factor}%)
* **Dual-Port Level 2 Smart EV Chargers:** {num_ev_chargers} ports (capable of powering faculty EVs and future electric school buses)

---

## 3. Federal IRA Section 6417 Elective Pay Breakdown
Under 26 U.S.C. § 6417 and IRS Treasury Decision 9988, local public school districts operate as applicable tax-exempt entities eligible for elective payment:

| Incentive Component | Statutory Credit Rate | Applied Status | Value ($) |
| :--- | :--- | :--- | :--- |
| **Base Clean Energy Investment Tax Credit (ITC)** | 30.0% | Applicable to all public schools | ${(total_cost * 0.30):,.2f} |
| **Domestic Content Bonus (26 U.S.C. § 48(a)(12))** | +10.0% | Steel canopy & domestic modules | ${(total_cost * (0.10 if fin_metrics.get('domestic_bonus_pct', 0) > 0 else 0)):,.2f} |
| **Energy Community Bonus (26 U.S.C. § 48(a)(14))** | +10.0% | {'Eligible Census Tract' if school_info.get('energy_community') else 'Non-eligible'} | ${(total_cost * (0.10 if school_info.get('energy_community') else 0)):,.2f} |
| **Title I / Low-Income Bonus (26 U.S.C. § 48(e))** | +10.0% | {'Eligible Title I Campus' if school_info.get('is_title1') else 'Non-eligible'} | ${(total_cost * (0.10 if school_info.get('is_title1') else 0)):,.2f} |
| **TOTAL FEDERAL REIMBURSEMENT RATE** | **{ira_pct}.0%** | **Direct Cash Check via Form 990-T** | **${irs_check:,.2f}** |

---

## 4. Environmental, Health & Community Benefits
* **Annual Scope 2 Carbon Abatement:** **{co2_tons:,.1f} Metric Tons CO₂e / year**
* **Passenger Vehicle Equivalent:** **{cars_offset:,.0f} gasoline passenger vehicles removed** from the road annually
* **Urban Heat Island Reduction:** Shading {usable_canopy_m2:,.0f} m² of dark asphalt reduces pavement surface temperatures by 30°F–45°F during extreme heat events.
* **Campus Microgrid & Resilience Readiness:** Canopy infrastructure provides the physical foundation for adding battery energy storage (BESS) for clean air and emergency community cooling centers.

---

## 5. Model School Board Resolution Language
```text
WHEREAS, energy expenditures represent a significant non-instructional operating expense for the District; and
WHEREAS, Section 6417 of the federal Inflation Reduction Act allows tax-exempt public school districts to receive direct cash payments covering up to 50% of the cost of clean energy installations;
NOW, THEREFORE, BE IT RESOLVED that the Board of Education hereby directs the Superintendent and Chief Business Official to:
1. Complete IRS Pre-Filing Registration for clean energy elective pay under 26 CFR § 1.6417-5;
2. Authorize an RFP (Request for Proposals) for a parking lot solar canopy installation at {school_name};
3. Apply all net utility savings directly into instructional materials and teacher retention funds.
```

---

## 6. Regulatory References & Data Provenance
1. **26 U.S.C. § 6417 & IRS TD 9988:** *Clean Energy Elective Payment Regulations under Section 6417* (2024).
2. **National Laboratory of the Rockies (NLR / NREL):** *PVWatts v8 Solar Irradiance Physical Engine*.
3. **National Center for Education Statistics (NCES):** *EDGE Public School Geographic Locations 2023*.
4. **U.S. Energy Information Administration (EIA):** *Form 861 Commercial Electricity Rates by State (2024)*.
5. **U.S. Environmental Protection Agency (EPA):** *eGRID Summary Tables (2024)*.
"""
    return md
