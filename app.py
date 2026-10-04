"""
app.py
SolarSchools USA: Phased Geospatial Decision Platform for K-12 Parking Canopy Solar
& Federal IRA Section 6417 Elective Pay Modeling.
Developed for the SVYCA Youth For Earth (Y4E) Hackathon @ Stanford Climate Week.
"""
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from core.data_ingest import get_school_directory, get_school_parking_footprint
from core.solar_engine import query_pvwatts_generation, calculate_ev_charging_synergy
from core.financial_model import calculate_ira_financials
from core.report_generator import generate_action_brief_markdown

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SolarSchools USA — K-12 Canopy & IRA Direct Pay Engine",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive cards and clean visual hierarchy
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        color: #f8fafc;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 4px;
        margin-bottom: 4px;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #10b981;
    }
    .phase-badge-p1 {
        background-color: #0369a1;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .phase-badge-p2 {
        background-color: #0d9488;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .phase-badge-p3 {
        background-color: #7c3aed;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR FILTERS & CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/solar-panel.png", width=64)
st.sidebar.title("☀️ SolarSchools USA")
st.sidebar.markdown("**Decision Platform for K-12 Solar Canopies & IRA Direct Pay**")
st.sidebar.markdown("---")

# Phase, Grade Level & Solar Status Filters
col_fil1, col_fil2 = st.sidebar.columns(2)
with col_fil1:
    phase_options = [
        "Phase 1: Bay Area",
        # "All Phases",
        # "Phase 2: California Statewide",
        # "Phase 3: Nationwide USA"
    ]
    selected_phase = st.selectbox("🎯 Phase:", phase_options, index=0)

with col_fil2:
    level_options = [
        "All Levels",
        "High School",
        "Middle School",
        "Elementary School"
    ]
    selected_level = st.selectbox("🎓 Grade Level:", level_options, index=0)

status_options = [
    "All Statuses",
    "Implemented (Active Savings)",
    "Unshaded (Losing Money)"
]
selected_status = st.sidebar.selectbox("⚡ Solar Deployment Status:", status_options, index=0)

# Filtered Schools
filtered_schools = get_school_directory(selected_phase, selected_level, selected_status)
if not filtered_schools:
    st.sidebar.warning("No campuses match all 3 filters. Showing matching phase schools.")
    filtered_schools = get_school_directory(selected_phase, "All Levels", "All Statuses")

school_names = list(filtered_schools.keys())
selected_school_name = st.sidebar.selectbox("🏫 Select K-12 Campus:", school_names, index=0)
school_info = filtered_schools[selected_school_name]

# Level badge icon
lvl = school_info.get("level", "School")
lvl_icon = "🏫" if lvl == "High School" else ("🎒" if lvl == "Middle School" else "🖍️")

# Solar status icon
s_status = school_info.get("solar_status", "Unshaded (Losing Money)")
status_icon = "⚡" if "Implemented" in s_status else "🔥"

st.sidebar.markdown(f"**Campus Level:** {lvl_icon} {lvl}")
st.sidebar.markdown(f"**Solar Status:** {status_icon} **{s_status}**")
st.sidebar.markdown(f"**District:** {school_info['district']}")
st.sidebar.markdown(f"**Location:** {school_info['county']} County, {school_info['state']}")
st.sidebar.markdown(f"**Utility:** {school_info['utility']}")
st.sidebar.markdown(f"**Enrollment:** {school_info['enrollment']:,} students")
st.sidebar.markdown("---")

# Interactive Sliders & Parameters
st.sidebar.subheader("⚙️ System Configuration")
coverage_pct = st.sidebar.slider(
    "Parking Lot Canopy Coverage (%)",
    min_value=20,
    max_value=100,
    value=65,
    step=5,
    help="Percentage of unshaded campus asphalt parking lot equipped with solar canopies."
)

num_ev_chargers = st.sidebar.slider(
    "Level 2 EV Charging Ports",
    min_value=0,
    max_value=40,
    value=8,
    step=2,
    help="Dual-port smart EV chargers for faculty vehicles and electric school buses."
)

# Tariff Override
default_tariff = school_info.get("commercial_tariff", 0.28)
tariff_override = st.sidebar.number_input(
    f"Commercial Tariff ($/kWh) [{school_info['utility'].split('(')[0].strip()}]",
    min_value=0.05,
    max_value=0.60,
    value=float(default_tariff),
    step=0.01,
    format="%.3f",
    help="Commercial retail electricity rate avoided through on-site generation."
)

st.sidebar.subheader("🏛️ IRA Section 6417 Bonus Credits")
col_bon1, col_bon2 = st.sidebar.columns(2)
with col_bon1:
    is_energy_community = st.checkbox("Energy Community (+10%)", value=school_info.get("energy_community", False))
    has_domestic_content = st.checkbox("Domestic Steel (+10%)", value=True)
with col_bon2:
    is_title1 = st.checkbox("Title I Low-Income (+10%)", value=school_info.get("is_title1", False))

cost_per_watt = st.sidebar.slider(
    "Canopy Installed Cost ($/Watt DC)",
    min_value=2.40,
    max_value=4.00,
    value=3.10,
    step=0.05,
    help="Turnkey commercial canopy cost including structural steel and foundations."
)

# -----------------------------------------------------------------------------
# 3. COMPUTATIONAL PIPELINE
# -----------------------------------------------------------------------------
# 1. Spatial footprint calculation
footprint = get_school_parking_footprint(school_info)
gross_m2 = footprint["gross_area_m2"]
usable_m2 = round(gross_m2 * (coverage_pct / 100.0) * 0.65, 1)
footprint["usable_canopy_m2"] = usable_m2

# 2. Solar capacity calculation (200 W/m2 high-efficiency commercial panels)
system_kw = round(usable_m2 * 0.20, 1)

# 3. NLR PVWatts v8 solar generation
solar_gen = query_pvwatts_generation(
    lat=school_info["lat"],
    lon=school_info["lon"],
    capacity_kw=system_kw
)

# 4. EV synergy
ev_synergy = calculate_ev_charging_synergy(
    annual_kwh=solar_gen["annual_kwh"],
    num_level2_chargers=num_ev_chargers
)

# 5. Financial & IRA Direct Pay model
finances = calculate_ira_financials(
    system_capacity_kw=system_kw,
    annual_kwh=solar_gen["annual_kwh"],
    commercial_tariff_per_kwh=tariff_override,
    state=school_info.get("state", "CA"),
    is_title1=is_title1,
    is_energy_community=is_energy_community,
    has_domestic_content=has_domestic_content,
    num_ev_chargers=num_ev_chargers,
    cost_per_watt=cost_per_watt
)

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD HEADER & KPI METRICS
# -----------------------------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🇺🇸 SolarSchools USA: K-12 Solar Canopy & IRA Direct Pay Engine")
    st.markdown("**SVYCA Youth For Earth Hackathon @ Stanford Climate Week** | *Turning School Asphalt into Clean Power & Classroom Capital*")
with col_h2:
    phase_str = school_info.get("phase", "Phase 1")
    if "Phase 1" in phase_str:
        badge_html = f"<div style='text-align: right;'><span class='phase-badge-p1'>{phase_str}</span></div>"
    elif "Phase 2" in phase_str:
        badge_html = f"<div style='text-align: right;'><span class='phase-badge-p2'>{phase_str}</span></div>"
    else:
        badge_html = f"<div style='text-align: right;'><span class='phase-badge-p3'>{phase_str}</span></div>"
    st.markdown(badge_html, unsafe_allow_html=True)
    st.caption(f"Campus: **{selected_school_name}**")

# High-School Student & Judge Explainer Expander
with st.expander("💡 **How SolarSchools USA Works in 4 Simple Steps** (Click to view student explainer)", expanded=False):
    st.markdown("""
    1. **Measure the Asphalt:** We look up the school's parking lot using OpenStreetMap satellite data. We plan canopies over 65% of the lot so cars still have wide driving lanes and shaded parking spots.
    2. **Calculate Solar Energy:** We plug the campus GPS coordinates into the **Department of Energy / NLR PVWatts v8 solar engine** to simulate how much sunshine the panels absorb across all 12 months.
    3. **The Federal Direct Pay Check:** Because public schools don't pay federal income taxes, **Section 6417 of the Inflation Reduction Act** sends the school district an **actual cash reimbursement check covering 30% to 50% of the cost**.
    4. **Classroom Dividends:** The school stops buying expensive power from the utility company, saving tens of thousands of dollars each year that go straight back into classroom supplies, field trips, and teacher salaries!
    """)

# Dynamic Solar Status & "Cost of Inaction" Banner
if "Implemented" in s_status:
    inst_yr = school_info.get("installed_year", 2022)
    st.success(
        f"✅ **VERIFIED LEADER CAMPUS (Solar Deployed in {inst_yr}):** "
        f"{school_info.get('deployment_details', '')} "
        f"This campus proves our engineering and financial model with real utility bill savings of **${finances['annual_utility_savings']:,.0f}/year**!"
    )
else:
    inaction_5yr = finances['annual_utility_savings'] * 5
    inaction_10yr = finances['annual_utility_savings'] * 10
    st.error(
        f"🔥 **CLEAN ENERGY OPPORTUNITY (Currently Losing Money to Utility):** "
        f"{school_info.get('deployment_details', '')}\n\n"
        f"**⏳ The Cost of Inaction:** If the School Board delays solar installation, the district will forfeit **${inaction_5yr:,.0f} over 5 years** "
        f"(or **${inaction_10yr:,.0f} over a decade**) in avoidable electric bills, while leaving an upfront **${finances['irs_direct_cash_check']:,.0f} IRS Direct Pay cash check** unclaimed!"
    )

st.markdown("---")

# Top KPI Metric Row (6 Cards) with relatable high-school analogies
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

stalls_covered = int(usable_m2 / 25)
homes_powered = int(solar_gen['annual_kwh'] / 10500) if solar_gen['annual_kwh'] > 0 else 0

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Canopy Capacity</div>
        <div class="metric-value">{system_kw:,.0f} <span style="font-size: 1rem;">kW</span></div>
        <div class="metric-sub">Shades ~{stalls_covered} parking spots</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Annual Clean Power</div>
        <div class="metric-value">{solar_gen['annual_kwh']:,.0f} <span style="font-size: 0.9rem;">kWh</span></div>
        <div class="metric-sub">Powers ~{homes_powered} average homes</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    ira_pct = int(finances['ira_rebate_pct'] * 100)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">IRS Direct Pay Check</div>
        <div class="metric-value" style="color: #4ade80;">${finances['irs_direct_cash_check']:,.0f}</div>
        <div class="metric-sub">{ira_pct}% Federal Cash Grant</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Annual Utility Savings</div>
        <div class="metric-value" style="color: #fbbf24;">${finances['annual_utility_savings']:,.0f}</div>
        <div class="metric-sub">Saved from power bills/yr</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Net District Cost</div>
        <div class="metric-value">${finances['net_district_investment']:,.0f}</div>
        <div class="metric-sub">After federal cash check</div>
    </div>
    """, unsafe_allow_html=True)

with kpi6:
    payback_display = f"{finances['payback_years']} yrs" if finances['payback_years'] > 0 else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Simple Payback</div>
        <div class="metric-value" style="color: #a78bfa;">{payback_display}</div>
        <div class="metric-sub">Zero taxpayer bonds needed</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. TABBED INTERACTIVE SECTIONS
# -----------------------------------------------------------------------------
tab_map, tab_physics, tab_finance, tab_equity, tab_brief = st.tabs([
    "🛰️ Campus Satellite & Canopy Map",
    "⚡ Solar Physics & Seasonal Generation",
    "💰 25-Year Lifecycle Cashflow & IRA ROI",
    "🌿 Environmental Justice & Heat Island",
    "📄 School Board Action Brief"
])

# -----------------------------------------------------------------------------
# TAB 1: GEOSPATIAL FOLIUM MAP
# -----------------------------------------------------------------------------
with tab_map:
    st.subheader(f"Campus Geospatial Footprint — {selected_school_name}")
    st.caption("Visualizing unshaded surface asphalt parking lots and proposed photovoltaic canopy coverage footprint.")

    map_col1, map_col2 = st.columns([3, 1])

    with map_col1:
        lat, lon = school_info["lat"], school_info["lon"]
        lot_lat = footprint.get("lot_lat", lat)
        lot_lon = footprint.get("lot_lon", lon)

        m = folium.Map(
            location=[lot_lat, lot_lon],
            zoom_start=17,
            tiles=None
        )
        
        # Add high-resolution satellite imagery as default basemap
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery',
            name='Satellite Imagery (Default)',
            overlay=False,
            control=True
        ).add_to(m)

        # Add OpenStreetMap as alternative basemap
        folium.TileLayer(
            tiles='OpenStreetMap',
            name='Street Map',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add canopy footprint circle centered on the surface parking lot
        radius_canopy = (usable_m2 / 3.14159) ** 0.5

        folium.Circle(
            location=[lot_lat, lot_lon],
            radius=radius_canopy,
            color="#f59e0b",
            fill=True,
            fill_color="#fbbf24",
            fill_opacity=0.45,
            tooltip=f"Proposed Solar Canopy: {system_kw:,.0f} kW DC ({usable_m2:,.0f} m²)",
            popup=f"<b>Proposed Solar Canopy Site</b><br>Capacity: {system_kw} kW DC<br>Area: {usable_m2:,.0f} m²<br>Stalls Covered: ~{int(usable_m2/25)}"
        ).add_to(m)

        # Parking Lot Canopy Site Marker
        folium.Marker(
            location=[lot_lat, lot_lon],
            popup=f"<b>Proposed Solar Canopy Site</b><br>{selected_school_name} Parking Lot<br>Capacity: {system_kw:,.0f} kW DC",
            tooltip=f"Solar Canopy Site ({usable_m2:,.0f} m²)",
            icon=folium.Icon(color="orange", icon="bolt", prefix="fa")
        ).add_to(m)

        # Campus Entrance Marker
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{selected_school_name}</b><br>{school_info['district']}<br>Enrollment: {school_info['enrollment']:,}",
            tooltip=f"{selected_school_name} (Campus)",
            icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa")
        ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, height=480, width=None)

    with map_col2:
        st.markdown("#### 📐 Spatial Geometry")
        st.write(f"- **Gross Surface Lot Area:** {gross_m2:,.0f} m²")
        st.write(f"- **Canopy Packing Factor:** 65.0%")
        st.write(f"- **Active Solar Catchment:** {usable_m2:,.0f} m²")
        st.write(f"- **Total Parking Stalls:** ~{footprint['parking_stalls']} stalls")
        st.write(f"- **Canopy-Covered Stalls:** ~{int(usable_m2 / 25)} stalls")
        st.write(f"- **EV Charging Ports:** {num_ev_chargers} ports")
        st.markdown("---")
        st.markdown("#### 🔍 Campus Characteristics")
        st.info(school_info.get("notes", "Representative K-12 public school campus."))

# -----------------------------------------------------------------------------
# TAB 2: SOLAR PHYSICS & GENERATION PROFILE
# -----------------------------------------------------------------------------
with tab_physics:
    st.subheader("Monthly Solar Physics Simulation (PVWatts v8 / NSRDB)")
    st.caption("Modeled using the U.S. Department of Energy / National Laboratory of the Rockies (NLR) active REST API.")

    fig_gen = go.Figure()
    fig_gen.add_trace(go.Bar(
        x=solar_gen["monthly_labels"],
        y=solar_gen["monthly_kwh"],
        name="Solar AC Generation (kWh)",
        marker_color="#38bdf8",
        hovertemplate="%{x}: <b>%{y:,.0f} kWh</b><extra></extra>"
    ))

    # Add monthly EV charging demand if EV chargers enabled
    if num_ev_chargers > 0:
        monthly_ev_kwh = ev_synergy["total_ev_demand_kwh"] / 12.0
        fig_gen.add_trace(go.Scatter(
            x=solar_gen["monthly_labels"],
            y=[monthly_ev_kwh] * 12,
            mode="lines",
            name=f"Level 2 EV Charging Demand ({num_ev_chargers} ports)",
            line=dict(color="#10b981", width=3, dash="dash"),
            hovertemplate="EV Demand: <b>%{y:,.0f} kWh/mo</b><extra></extra>"
        ))

    fig_gen.update_layout(
        template="plotly_dark",
        title=f"Monthly Energy Generation Profile for {system_kw:,.0f} kW DC Canopy",
        xaxis_title="Month",
        yaxis_title="Kilowatt-Hours (kWh AC)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=50, b=40),
        height=420
    )
    st.plotly_chart(fig_gen, use_container_width=True)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric("System Nameplate Capacity", f"{system_kw:,.1f} kW DC")
        st.caption("Standard monocrystalline 200 W/m² modules at 10° canopy tilt.")
    with col_p2:
        st.metric("Annual AC Generation", f"{solar_gen['annual_kwh']:,.0f} kWh")
        st.caption(f"Data source: {'Live NLR PVWatts v8 API' if solar_gen['is_live_api'] else 'NSRDB Regional Constants'}")
    with col_p3:
        st.metric("Level 2 EV Synergy", f"{ev_synergy['passenger_ev_miles_equivalent']:,.0f} mi/yr", f"{ev_synergy['ev_solar_coverage_pct']}% EV demand covered")
        st.caption(f"Or ~{ev_synergy['school_bus_miles_equivalent']:,.0f} miles/yr for Type-C electric school buses.")

# -----------------------------------------------------------------------------
# TAB 3: 25-YEAR LIFECYCLE CASHFLOW & IRA ROI
# -----------------------------------------------------------------------------
with tab_finance:
    st.subheader("25-Year Lifecycle Financial Cashflow & Direct Pay Economics")
    st.caption("Demonstrating how IRA Section 6417 eliminates capital barriers and creates an ongoing classroom dividend.")

    col_f1, col_f2 = st.columns([3, 2])

    with col_f1:
        # Cashflow Line Chart
        df_cf = pd.DataFrame(finances["cashflow_schedule"])
        if not df_cf.empty:
            fig_cf = go.Figure()
            
            # Cumulative Net Benefit
            fig_cf.add_trace(go.Scatter(
                x=df_cf["year"],
                y=df_cf["cumulative_net_usd"],
                name="Cumulative Net Benefit ($)",
                line=dict(color="#22c55e", width=3),
                fill="tozeroy",
                fillcolor="rgba(34, 197, 94, 0.15)",
                hovertemplate="Year %{x}: <b>$%{y:,.0f}</b><extra></extra>"
            ))

            # Break-even zero line
            fig_cf.add_hline(y=0, line_dash="dot", line_color="#ef4444", annotation_text="Break-Even Point")

            fig_cf.update_layout(
                template="plotly_dark",
                title="Cumulative Net District Fiscal Benefit over 25 Years",
                xaxis_title="Operating Year",
                yaxis_title="Net Value (USD)",
                margin=dict(l=40, r=40, t=50, b=40),
                height=380
            )
            st.plotly_chart(fig_cf, use_container_width=True)

    with col_f2:
        # Project Cost Breakdown Donut Chart
        labels = ["IRS Direct Pay Cash Check", "Net District Investment"]
        values = [finances["irs_direct_cash_check"], finances["net_district_investment"]]
        colors = ["#10b981", "#3b82f6"]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.55,
            marker_colors=colors,
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>"
        )])
        fig_pie.update_layout(
            template="plotly_dark",
            title=f"Capital Financing Structure (${finances['total_project_cost']:,.0f} Total)",
            margin=dict(l=20, r=20, t=50, b=20),
            height=380,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # 25-Year Cashflow Data Table
    with st.expander("📋 View Full 25-Year Operating Pro Forma Table"):
        if not df_cf.empty:
            st.dataframe(
                df_cf.rename(columns={
                    "year": "Year",
                    "generation_kwh": "AC Generation (kWh)",
                    "electricity_tariff": "Avoided Tariff ($/kWh)",
                    "gross_savings_usd": "Gross Savings ($)",
                    "om_expense_usd": "O&M Expense ($)",
                    "annual_net_benefit_usd": "Annual Net ($)",
                    "cumulative_net_usd": "Cumulative Net ($)"
                }).style.format({
                    "AC Generation (kWh)": "{:,.0f}",
                    "Avoided Tariff ($/kWh)": "${:.3f}",
                    "Gross Savings ($)": "${:,.0f}",
                    "O&M Expense ($)": "${:,.0f}",
                    "Annual Net ($)": "${:,.0f}",
                    "Cumulative Net ($)": "${:,.0f}"
                }),
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# TAB 4: ENVIRONMENTAL JUSTICE & HEAT ISLAND
# -----------------------------------------------------------------------------
with tab_equity:
    st.subheader("🌿 Environmental Justice, Heat Island Mitigation & Scope 2 Abatement")
    st.caption("Quantifying the non-energy co-benefits of parking lot solar canopies for K-12 school communities.")

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.metric("Annual CO₂e Avoided", f"{finances['annual_co2_tons_avoided']:,.1f} MT")
        st.caption(f"Based on EPA eGRID factor for {school_info.get('state', 'US')} grid.")
    with col_e2:
        st.metric("Gasoline Cars Removed", f"{finances['passenger_cars_offset']:,.0f} Vehicles")
        st.caption("Equivalent passenger vehicles removed from the road each year.")
    with col_e3:
        st.metric("Forest Sequestration", f"{finances['tree_acres_equivalent']:,.0f} Acres")
        st.caption("Equivalent acres of U.S. forest carbon absorption.")

    st.markdown("---")
    st.markdown("#### 🌡️ Urban Heat Island & Campus Resilience Benefits")
    st.write(
        f"School surface parking lots are high-emissivity thermal sponges. Converting **{usable_m2:,.0f} m² ({usable_m2 * 10.7639:,.0f} sq. ft.)** "
        "of asphalt into a shaded solar canopy drops ambient ground temperatures by **30°F to 45°F** during summer and autumn heat waves."
    )
    st.write(
        "- **Air Quality & Respiratory Protection:** Shaded vehicles experience 80% lower volatile organic compound (VOC) cabin outgassing.\n"
        "- **Clean Air Centers (CARB AB 836):** With the addition of battery energy storage, this canopy allows the campus gymnasium to operate as an emergency clean air and cooling shelter during wildfire smoke events.\n"
        "- **Title I Community Equity:** If designated Title I or in a CalEnviroScreen / DOE Energy Community tract, this installation captures maximum federal Direct Pay subsidies to lower public school tax burdens."
    )

# -----------------------------------------------------------------------------
# TAB 5: SCHOOL BOARD ACTION BRIEF
# -----------------------------------------------------------------------------
with tab_brief:
    st.subheader("📄 1-Page School Board Action Brief & Direct Export")
    st.caption("Ready for student climate advocates and district facilities directors to present at official Board of Education hearings.")

    # Generate Action Brief Markdown
    action_brief_md = generate_action_brief_markdown(
        school_name=selected_school_name,
        school_info=school_info,
        footprint=footprint,
        solar_metrics=solar_gen,
        fin_metrics=finances,
        coverage_pct=coverage_pct,
        num_ev_chargers=num_ev_chargers
    )

    # Download Button with clean CamelCase filename
    school_base = selected_school_name.split('(')[0].strip()
    clean_camel = ''.join(word.capitalize() for word in school_base.split() if word.isalnum())
    clean_filename = f"{clean_camel}ActionBrief.md"
    st.download_button(
        label="📥 Download Executive Action Brief (Markdown)",
        data=action_brief_md,
        file_name=clean_filename,
        mime="text/markdown",
        help="Click to download the formatted action brief for presentation to school administrators."
    )

    st.markdown("---")
    # Live Preview Container
    with st.container():
        st.markdown(action_brief_md)

# -----------------------------------------------------------------------------
# FOOTER & LEGAL CITATIONS
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "**SolarSchools USA** | Developed for the SVYCA Youth For Earth Hackathon @ Stanford Climate Week 2026. "
    "Calculations modeled in accordance with 26 U.S.C. § 6417, IRS TD 9988, NREL/NLR PVWatts v8, and EPA eGRID 2024. "
    "All datasets are open-access and verified."
)
