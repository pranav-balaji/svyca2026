# SolarSchools USA
# Copyright (c) 2026 Pranav Balaji
# SPDX-License-Identifier: Apache-2.0
"""
core/solar_engine.py
Integrates with the U.S. Department of Energy / National Laboratory of the Rockies (NLR)
PVWatts v8 REST API for solar irradiance and AC kilowatt-hour modeling, with resilient
regional fallback algorithms for offline or demo operations.
"""
import os
import requests
from typing import Dict, Any, List

# Official active federal endpoint (replaces retired developer.nrel.gov)
PVWATTS_API_URL = "https://developer.nlr.gov/api/pvwatts/v8.json"
DEFAULT_API_KEY = os.environ.get("NLR_API_KEY", "DEMO_KEY")

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Normalized monthly solar distribution curves by latitude band (used for fallback modeling)
MONTHLY_DISTRIBUTION_PATTERNS = {
    "sunbelt": [0.065, 0.072, 0.088, 0.098, 0.108, 0.112, 0.110, 0.102, 0.090, 0.078, 0.065, 0.062],
    "temperate": [0.048, 0.058, 0.082, 0.098, 0.115, 0.125, 0.124, 0.112, 0.094, 0.072, 0.050, 0.042],
    "northern": [0.038, 0.050, 0.080, 0.102, 0.122, 0.134, 0.132, 0.118, 0.092, 0.068, 0.042, 0.032],
}


def query_pvwatts_generation(
    lat: float,
    lon: float,
    capacity_kw: float,
    api_key: str = DEFAULT_API_KEY,
    tilt: float = 10.0,
    azimuth: float = 180.0,
    array_type: int = 2,      # 2 = Fixed roof mount / canopy
    module_type: int = 1,     # 1 = Premium monocrystalline
    losses: float = 14.0      # Standard commercial derate
) -> Dict[str, Any]:
    """
    Queries PVWatts v8 API for AC generation metrics.
    If the API call fails or times out, falls back to regional NSRDB solar harvest constants.
    """
    if capacity_kw <= 0:
        return {
            "annual_kwh": 0.0,
            "capacity_factor": 0.0,
            "monthly_kwh": [0.0] * 12,
            "monthly_labels": MONTH_NAMES,
            "is_live_api": False,
            "error_msg": "Capacity must be greater than zero."
        }

    params = {
        "api_key": api_key,
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "system_capacity": round(capacity_kw, 2),
        "azimuth": azimuth,
        "tilt": tilt,
        "array_type": array_type,
        "module_type": module_type,
        "losses": losses
    }

    try:
        response = requests.get(PVWATTS_API_URL, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            outputs = data.get("outputs", {})
            ac_annual = float(outputs.get("ac_annual", 0.0))
            cap_factor = float(outputs.get("capacity_factor", 0.0))
            ac_monthly = [round(float(m), 1) for m in outputs.get("ac_monthly", [])]

            if ac_annual > 0 and len(ac_monthly) == 12:
                return {
                    "annual_kwh": round(ac_annual, 1),
                    "capacity_factor": round(cap_factor, 2),
                    "monthly_kwh": ac_monthly,
                    "monthly_labels": MONTH_NAMES,
                    "is_live_api": True,
                    "error_msg": None
                }
    except Exception as e:
        # Gracefully handle API timeout or network hiccups
        pass

    # --- Resilient Fallback Calculation ---
    # Multiplier in kWh AC per kW DC installed per year based on latitude
    if lat < 34.0:
        harvest_multiplier = 1650.0  # Sunbelt (TX, AZ, FL, SoCal)
        dist_key = "sunbelt"
    elif lat < 40.0:
        harvest_multiplier = 1460.0  # Central CA, Mid-Atlantic
        dist_key = "temperate"
    else:
        harvest_multiplier = 1320.0  # Midwest, Northeast, Pacific NW
        dist_key = "northern"

    annual_kwh = round(capacity_kw * harvest_multiplier, 1)
    cap_factor = round((harvest_multiplier / 8760.0) * 100.0, 2)
    distribution = MONTHLY_DISTRIBUTION_PATTERNS[dist_key]
    monthly_kwh = [round(annual_kwh * weight, 1) for weight in distribution]

    return {
        "annual_kwh": annual_kwh,
        "capacity_factor": cap_factor,
        "monthly_kwh": monthly_kwh,
        "monthly_labels": MONTH_NAMES,
        "is_live_api": False,
        "error_msg": "Used empirical NSRDB regional fallback."
    }


def calculate_ev_charging_synergy(annual_kwh: float, num_level2_chargers: int = 8) -> Dict[str, Any]:
    """
    Models integration of on-site solar canopy generation with Level 2 EV charging infrastructure,
    such as faculty commuter parking and electric school buses.
    """
    # Average commercial Level 2 charger: 7.2 kW, operating ~4 hours/school day (~200 school days)
    # Energy consumed per charger: ~5,760 kWh/year
    annual_demand_per_charger = 5760.0
    total_ev_demand_kwh = round(num_level2_chargers * annual_demand_per_charger, 1)

    ev_solar_coverage_pct = round((min(annual_kwh, total_ev_demand_kwh) / total_ev_demand_kwh * 100), 1) if total_ev_demand_kwh > 0 else 100.0
    
    # 1 kWh ~ 3.5 miles for an electric passenger vehicle
    # 1 kWh ~ 0.55 miles for a Type C electric school bus
    passenger_ev_miles = round(annual_kwh * 3.5, 0)
    electric_school_bus_miles = round(annual_kwh * 0.55, 0)

    return {
        "num_chargers": num_level2_chargers,
        "total_ev_demand_kwh": total_ev_demand_kwh,
        "ev_solar_coverage_pct": ev_solar_coverage_pct,
        "passenger_ev_miles_equivalent": passenger_ev_miles,
        "school_bus_miles_equivalent": electric_school_bus_miles
    }
