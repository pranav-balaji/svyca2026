# SolarSchools USA
# Copyright (c) 2026 Pranav Balaji and SolarSchools USA Contributors
# SPDX-License-Identifier: MIT
"""
SolarSchools USA: Core Computational Modules
"""
from .data_ingest import get_school_parking_footprint, get_school_directory, SCHOOL_DATABASE
from .solar_engine import query_pvwatts_generation, calculate_ev_charging_synergy
from .financial_model import calculate_ira_financials
from .report_generator import generate_action_brief_markdown

__all__ = [
    "get_school_parking_footprint",
    "get_school_directory",
    "SCHOOL_DATABASE",
    "query_pvwatts_generation",
    "calculate_ev_charging_synergy",
    "calculate_ira_financials",
    "generate_action_brief_markdown"
]
