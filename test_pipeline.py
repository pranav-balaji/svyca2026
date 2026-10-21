# SolarSchools USA
# Copyright (c) 2026 Pranav Balaji
# SPDX-License-Identifier: MIT
"""
test_pipeline.py
Unit tests verifying core modules for SolarSchools USA.
"""
import core.data_ingest as di
import core.solar_engine as se
import core.financial_model as fm
import core.report_generator as rg


def test_core_pipeline():
    print("Testing school directory...")
    schools = di.get_school_directory()
    assert len(schools) >= 10, f"Expected at least 10 schools, got {len(schools)}"
    print(f"Total schools: {len(schools)}")

    phases = [
        "Phase 1: Bay Area",
        # "Phase 2: California Statewide",
        # "Phase 3: Nationwide USA"
    ]
    for phase in phases:
        filtered = di.get_school_directory(phase)
        assert len(filtered) > 0, f"No schools found for phase: {phase}"
        print(f"  {phase}: {len(filtered)} schools")

    test_cases = [
        "Palo Alto High School (Palo Alto, CA)",
        "Monta Vista High School (Cupertino, CA)",
        "John F. Kennedy Middle School (Cupertino, CA)",
        "Stevens Creek Elementary School (Cupertino, CA)",
        # "Westlake High School (Austin, Texas)"
    ]

    for sname in test_cases:
        sinfo = schools[sname]
        print(f"\nEvaluating: {sname} ({sinfo['phase']})")
        
        # Test footprint
        fp = di.get_school_parking_footprint(sinfo)
        assert fp["gross_area_m2"] > 0
        usable_m2 = fp["gross_area_m2"] * 0.65 * 0.65
        system_kw = usable_m2 * 0.20
        
        # Test PVWatts engine
        sol = se.query_pvwatts_generation(sinfo["lat"], sinfo["lon"], system_kw)
        assert sol["annual_kwh"] > 0
        assert len(sol["monthly_kwh"]) == 12
        print(f"  System kW: {system_kw:,.1f} kW | Annual Gen: {sol['annual_kwh']:,.0f} kWh (Live API: {sol['is_live_api']})")

        # Test EV synergy
        ev = se.calculate_ev_charging_synergy(sol["annual_kwh"], 8)
        assert ev["passenger_ev_miles_equivalent"] > 0

        # Test Financial model
        fin = fm.calculate_ira_financials(
            system_capacity_kw=system_kw,
            annual_kwh=sol["annual_kwh"],
            commercial_tariff_per_kwh=sinfo["commercial_tariff"],
            state=sinfo["state"],
            is_title1=sinfo["is_title1"],
            is_energy_community=sinfo["energy_community"]
        )
        assert fin["total_project_cost"] > 0
        assert fin["irs_direct_cash_check"] > 0
        assert fin["payback_years"] > 0
        assert len(fin["cashflow_schedule"]) == 25
        print(f"  Turnkey Cost: ${fin['total_project_cost']:,.0f} | IRS Direct Pay Check: ${fin['irs_direct_cash_check']:,.0f}")
        print(f"  Net District Outlay: ${fin['net_district_investment']:,.0f} | Payback: {fin['payback_years']} yrs")
        print(f"  25-Yr Net Dividend: ${fin['lifetime_25yr_net_dividend']:,.0f}")

        # Test Action Brief generator
        brief = rg.generate_action_brief_markdown(sname, sinfo, fp, sol, fin, 65, 8)
        assert len(brief) > 500
        assert "School Board Action Brief" in brief
        print(f"  Action brief generated successfully ({len(brief):,} bytes)")

    print("\nAll unit tests PASSED successfully!")


if __name__ == "__main__":
    test_core_pipeline()
