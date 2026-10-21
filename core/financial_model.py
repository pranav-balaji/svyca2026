# SolarSchools USA
# Copyright (c) 2026 Pranav Balaji and SolarSchools USA Contributors
# SPDX-License-Identifier: MIT
"""
core/financial_model.py
Models Inflation Reduction Act (IRA) Section 6417 Elective Pay (Direct Pay),
turnkey solar canopy capital costs, utility tariff avoidance, and 25-year lifecycle cashflows.
"""
from typing import Dict, Any, List

# EPA eGRID CO2 emissions factors (lbs CO2 per kWh) by state/region
STATE_EMISSIONS_FACTORS = {
    "CA": 0.45,  # CAMX (Clean California Grid)
    "TX": 0.85,  # ERCT (Texas Interconnection)
    "AZ": 0.75,  # AZNM
    "FL": 0.82,  # FRCC
    "OH": 1.10,  # RFCW (Midwestern Coal-transition)
    "GA": 0.78,  # SRSO
    "DEFAULT": 0.85  # National average
}


def calculate_ira_financials(
    system_capacity_kw: float,
    annual_kwh: float,
    commercial_tariff_per_kwh: float,
    state: str = "CA",
    is_title1: bool = False,
    is_energy_community: bool = False,
    has_domestic_content: bool = True,
    num_ev_chargers: int = 0,
    cost_per_watt: float = 3.10
) -> Dict[str, Any]:
    """
    Computes turnkey capital requirements, IRS Section 6417 Direct Pay cash rebate,
    net district investment, utility savings, and 25-year lifecycle ROI.
    """
    if system_capacity_kw <= 0:
        return {
            "total_project_cost": 0.0,
            "canopy_solar_capex": 0.0,
            "ev_charging_capex": 0.0,
            "ira_rebate_pct": 0.30,
            "irs_direct_cash_check": 0.0,
            "net_district_investment": 0.0,
            "annual_utility_savings": 0.0,
            "payback_years": 0.0,
            "lifetime_25yr_net_dividend": 0.0,
            "annual_co2_tons_avoided": 0.0,
            "passenger_cars_offset": 0.0,
            "tree_acres_equivalent": 0.0,
            "cashflow_schedule": []
        }

    # 1. Capital Cost Model
    canopy_solar_capex = system_capacity_kw * 1000.0 * cost_per_watt
    # Dual-port commercial smart Level 2 charger: ~$6,000 per unit installed
    ev_charging_capex = num_ev_chargers * 6000.0
    total_project_cost = canopy_solar_capex + ev_charging_capex

    # 2. Federal IRA Section 6417 Direct Pay Breakdown
    # Base clean energy ITC rate = 30%
    base_credit = 0.30
    domestic_bonus = 0.10 if has_domestic_content else 0.0
    energy_comm_bonus = 0.10 if is_energy_community else 0.0
    title1_bonus = 0.10 if is_title1 else 0.0

    ira_rebate_pct = min(base_credit + domestic_bonus + energy_comm_bonus + title1_bonus, 0.60)
    irs_direct_cash_check = round(total_project_cost * ira_rebate_pct, 2)
    net_district_investment = round(total_project_cost - irs_direct_cash_check, 2)

    # 3. Annual Utility Savings & Simple Payback
    annual_utility_savings = round(annual_kwh * commercial_tariff_per_kwh, 2)
    payback_years = (
        round(net_district_investment / annual_utility_savings, 1)
        if annual_utility_savings > 0
        else 0.0
    )

    # 4. 25-Year Lifecycle Cashflow Projection
    # Panel degradation: 0.5%/year; Utility escalation: 2.5%/year; O&M: $15/kW-year (+2% inflation)
    degradation_rate = 0.005
    tariff_escalation = 0.025
    annual_om_per_kw = 15.0

    cashflow_schedule = []
    cumulative_net = -net_district_investment

    for yr in range(1, 26):
        degraded_gen = annual_kwh * ((1.0 - degradation_rate) ** (yr - 1))
        escalated_tariff = commercial_tariff_per_kwh * ((1.0 + tariff_escalation) ** (yr - 1))
        annual_gross_savings = degraded_gen * escalated_tariff
        annual_om = (system_capacity_kw * annual_om_per_kw) * ((1.0 + 0.02) ** (yr - 1))
        annual_net_benefit = annual_gross_savings - annual_om
        cumulative_net += annual_net_benefit

        cashflow_schedule.append({
            "year": yr,
            "generation_kwh": round(degraded_gen, 0),
            "electricity_tariff": round(escalated_tariff, 4),
            "gross_savings_usd": round(annual_gross_savings, 0),
            "om_expense_usd": round(annual_om, 0),
            "annual_net_benefit_usd": round(annual_net_benefit, 0),
            "cumulative_net_usd": round(cumulative_net, 0)
        })

    lifetime_25yr_net_dividend = round(cumulative_net, 2)

    # 5. Carbon Abatement & Environmental Equivalencies
    emission_factor = STATE_EMISSIONS_FACTORS.get(state.upper(), STATE_EMISSIONS_FACTORS["DEFAULT"])
    annual_co2_tons = round((annual_kwh * emission_factor) / 2204.62, 1)
    cars_offset = round(annual_co2_tons / 4.6, 1)  # EPA: 4.6 MT CO2/car-year
    tree_acres = round(annual_co2_tons / 0.82, 1)  # 1 acre US forest absorbs ~0.82 MT CO2/yr

    return {
        "total_project_cost": round(total_project_cost, 2),
        "canopy_solar_capex": round(canopy_solar_capex, 2),
        "ev_charging_capex": round(ev_charging_capex, 2),
        "base_credit_pct": base_credit,
        "domestic_bonus_pct": domestic_bonus,
        "energy_comm_bonus_pct": energy_comm_bonus,
        "title1_bonus_pct": title1_bonus,
        "ira_rebate_pct": round(ira_rebate_pct, 2),
        "irs_direct_cash_check": irs_direct_cash_check,
        "net_district_investment": net_district_investment,
        "annual_utility_savings": annual_utility_savings,
        "payback_years": payback_years,
        "lifetime_25yr_net_dividend": lifetime_25yr_net_dividend,
        "annual_co2_tons_avoided": annual_co2_tons,
        "passenger_cars_offset": cars_offset,
        "tree_acres_equivalent": tree_acres,
        "cashflow_schedule": cashflow_schedule
    }
