#!/usr/bin/env python3
# SolarSchools USA
# Copyright (c) 2026 Pranav Balaji
# SPDX-License-Identifier: Apache-2.0
"""
generate_docx.py
Converts DetailedDesignDocument.md into a beautifully styled Microsoft Word (.docx) document
with high-resolution color flowcharts, styled tables, formatted equations, and executive layout.
"""

import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_callout(doc, text, title=None, border_color="3B82F6", bg_color="EFF6FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=200, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    if title:
        run_title = p.add_run(title + "\n")
        run_title.bold = True
        run_title.font.name = "Calibri"
        run_title.font.size = Pt(10.5)
        run_title.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, headers, rows):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E3A8A")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.bold = True
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.add_row().cells
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = val
            set_cell_background(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
                
    # Column widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def build_word_document():
    doc = Document()
    
    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("SolarSchools USA: System Design Document")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run("Technical Architecture, API Workflows, Mathematical Models, and Defense Playbook")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    
    # Metadata Box
    meta_text = (
        "Author: Pranav Balaji\n"
        "Competition: SVYCA Youth For Earth Hackathon @ Stanford Climate Week (October 2026)\n"
        "Core Stack: Python 3.12, Streamlit, GeoPandas, Shapely, Folium, Plotly, Requests\n"
        "Target Audience: Hackathon Judges, School Board Officials, Student Climate Advocates"
    )
    add_callout(doc, meta_text, title="PROJECT METADATA", border_color="0284C7", bg_color="F0F9FF")
    
    # ---------------------------------------------------------------------------
    # Section 1: Table of Abbreviations & Core Terminology
    # ---------------------------------------------------------------------------
    h_abbr = doc.add_heading("1. Table of Abbreviations & Core Terminology", level=1)
    h_abbr.paragraph_format.space_before = Pt(14)
    h_abbr.paragraph_format.space_after = Pt(6)
    for run in h_abbr.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    tbl_gloss = doc.add_table(rows=1, cols=3)
    gloss_headers = ["Abbreviation", "Full Term / Agency", "Definition & Regulatory Role"]
    gloss_rows = [
        ["AC / DC", "Alternating / Direct Current", "DC is raw solar cell output; AC is usable building and grid electricity."],
        ["BBox", "Geographic Bounding Box", "Min/max latitude and longitude coordinates defining the spatial query boundary."],
        ["CDE", "California Department of Education", "State agency publishing California public school directories and enrollment records."],
        ["CRS / EPSG:4326", "Coordinate Reference System", "Global WGS 84 spherical coordinate reference system in decimal degrees."],
        ["EPA eGRID", "Emissions & Generation Resource Database", "Federal EPA database tracking subregion greenhouse gas emission factors per kWh."],
        ["EV", "Electric Vehicle", "Level 2 smart vehicle charging stations integrated into canopy steel columns."],
        ["IRA Direct Pay", "Inflation Reduction Act Section 6417", "Statutory mechanism providing 30% to 50% IRS cash refunds to tax-exempt entities."],
        ["IRS / Form 990-T", "Internal Revenue Service", "Federal tax agency; Form 990-T is filed by public school districts to claim Direct Pay."],
        ["K-12", "Kindergarten through 12th Grade", "The United States public primary and secondary education school system."],
        ["NCES", "National Center for Education Statistics", "Federal agency maintaining locations and demographic data for ~100k U.S. schools."],
        ["NLR / NSRDB", "National Laboratory of the Rockies", "U.S. DOE lab (formerly NREL) and the 4km National Solar Radiation Database."],
        ["POA", "Plane of Array", "Solar irradiance striking tilted photovoltaic collector surfaces."],
        ["Title I", "Federal Low-Income Designation", "Elementary & Secondary Education Act designation triggering +10% IRA bonus."],
        ["UTM", "Universal Transverse Mercator", "Conformal metric projection dividing the globe into 60 zones for accurate surface area (m2)."]
    ]
    format_table(tbl_gloss, [1.4, 2.2, 2.9], gloss_headers, gloss_rows)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------------------------
    # Section 2: Executive Summary & Design Rationale
    # ---------------------------------------------------------------------------
    h1 = doc.add_heading("2. Executive Summary & Design Rationale", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    for run in h1.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    doc.add_heading("2.1 Problem & Opportunity", level=2)
    p1 = doc.add_paragraph(style='List Bullet')
    p1.add_run("Energy Burden: ").bold = True
    p1.add_run("Public Kindergarten through 12th Grade (K-12) school districts spend over $8 billion annually on electricity, often their second-largest budget expense after personnel.")
    
    p2 = doc.add_paragraph(style='List Bullet')
    p2.add_run("Underutilized Asset: ").bold = True
    p2.add_run("Schools maintain extensive unshaded asphalt parking lots that intensify the urban heat island effect and increase cooling loads.")
    
    p3 = doc.add_paragraph(style='List Bullet')
    p3.add_run("Federal Catalyst: ").bold = True
    p3.add_run("Section 6417 of the federal Inflation Reduction Act (IRA) allows non-taxable entities—including public school districts—to receive elective cash payments ('Direct Pay') from the Internal Revenue Service (IRS) covering 30% to 50% of clean energy project costs.")
    
    p4 = doc.add_paragraph(style='List Bullet')
    p4.add_run("Access Barrier: ").bold = True
    p4.add_run("Commercial feasibility studies cost $15,000 to $50,000. SolarSchools USA provides a free, instant screening tool for student advocates and school boards.")
    
    doc.add_heading("2.2 Parking Canopies vs. Rooftop Solar", level=2)
    doc.add_paragraph("Commercial solar developers often suggest rooftop panels, but facilities directors face significant obstacles that parking lot canopies eliminate:")
    
    tbl_comp = doc.add_table(rows=1, cols=3)
    comp_headers = ["Evaluation Metric", "Rooftop Solar", "Parking Lot Canopy (SolarSchools USA)"]
    comp_rows = [
        ["Roof Warranty", "Risk of voiding 20-year membrane warranty", "Zero roof penetrations; independent structural steel"],
        ["Structural Capacity", "Limited by HVAC weight and seismic ratings", "Engineered independent pier foundations"],
        ["Microclimate Impact", "Minor roof cooling", "Drops asphalt surface temp by 30°F to 45°F"],
        ["EV Integration", "Requires expensive trenching to ground lot", "Turnkey conduit integration for Level 2 EV chargers"],
        ["Campus Visibility", "Hidden from student and community view", "Highly visible showcase of civic climate leadership"]
    ]
    format_table(tbl_comp, [1.5, 2.3, 2.7], comp_headers, comp_rows)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------------------------
    # Section 3
    # ---------------------------------------------------------------------------
    h2 = doc.add_heading("3. End-to-End System Architecture", level=1)
    h2.paragraph_format.space_before = Pt(14)
    for run in h2.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    doc.add_paragraph("The following architecture details the dataflow across user inputs, geospatial lookups, physical simulation APIs, financial models, and export layers.")
    
    # Embed Diagram 1
    if os.path.exists("assets/diagram_1.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture("assets/diagram_1.png", width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run("Figure 1: Full-Stack Modular System Architecture and Pipeline Dataflow")
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        
    # ---------------------------------------------------------------------------
    # Section 4
    # ---------------------------------------------------------------------------
    h3 = doc.add_heading("4. External API Workflows & Specifications", level=1)
    h3.paragraph_format.space_before = Pt(14)
    for run in h3.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    doc.add_paragraph("SolarSchools USA communicates with three external web services:")
    
    # Embed Diagram 2
    if os.path.exists("assets/diagram_2.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture("assets/diagram_2.png", width=Inches(5.5))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run("Figure 2: Tri-Service External API Integration Architecture")
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        
    doc.add_heading("3.1 National Laboratory of the Rockies (NLR / DOE) PVWatts v8 REST API", level=2)
    p_nlr_meta = doc.add_paragraph()
    p_nlr_meta.add_run("Agency: ").bold = True
    p_nlr_meta.add_run("U.S. Department of Energy / National Laboratory of the Rockies (NLR)\n")
    p_nlr_meta.add_run("Endpoint: ").bold = True
    p_nlr_meta.add_run("https://developer.nlr.gov/api/pvwatts/v8.json\n")
    p_nlr_meta.add_run("Method: ").bold = True
    p_nlr_meta.add_run("GET | ")
    p_nlr_meta.add_run("Implementation: ").bold = True
    p_nlr_meta.add_run("core/solar_engine.py")
    
    # Embed Diagram 3
    if os.path.exists("assets/diagram_3.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture("assets/diagram_3.png", width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run("Figure 3: PVWatts v8 API Request & Fallback Sequence Diagram")
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        
    doc.add_heading("Query Parameters", level=3)
    tbl_params = doc.add_table(rows=1, cols=4)
    param_headers = ["Parameter Key", "Type", "Value", "Engineering Rationale"]
    param_rows = [
        ["api_key", "string", "DEMO_KEY", "Federal API key for query quota tracking."],
        ["lat, lon", "float", "Decimal deg", "Geographic coordinates in WGS 84 (EPSG:4326)."],
        ["system_capacity", "float", "kW DC", "Nameplate capacity (usable_m2 x 0.20 kW/m2)."],
        ["azimuth", "float", "180", "True South orientation for optimal North American solar capture."],
        ["tilt", "float", "10", "10° carport tilt balancing drainage, wind load, and solar yield."],
        ["array_type", "integer", "2", "Fixed canopy / roof structure geometry."],
        ["module_type", "integer", "1", "Monocrystalline silicon modules (~20% nominal efficiency)."],
        ["losses", "float", "14.0", "Comprehensive aggregate system derate factor (14.0%)."]
    ]
    format_table(tbl_params, [1.3, 0.8, 1.1, 3.3], param_headers, param_rows)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    doc.add_heading("Aggregate System Derate Losses (14.0%)", level=3)
    p_derate = doc.add_paragraph()
    p_derate.add_run("To ensure conservative, bankable projections, the system applies a comprehensive 14.0% loss factor: Inverter conversion (4.0%), Temperature derate (3.0%), Soiling & dust (2.5%), Wiring resistance (2.0%), Module mismatch (1.5%), and Connection diodes (1.0%).")
    
    doc.add_heading("Fault-Tolerant Fallback Architecture", level=3)
    doc.add_paragraph("If the federal API exceeds 8 seconds or returns a non-200 code, an internal fallback algorithm derives solar yields from empirical National Solar Radiation Database (NSRDB) benchmarks: Sunbelt (<34° Lat) at 1,650 kWh/kW-yr, California / Mid-Latitude (34°-40°) at 1,460 kWh/kW-yr, and Northern (>40°) at 1,320 kWh/kW-yr distributed along a 12-month bell curve.")
    
    doc.add_heading("3.2 OpenStreetMap Spatial Vector Pipeline", level=2)
    doc.add_paragraph("Campus parking lots are queried via OSM vector ways (amenity=parking). Polygons are loaded into GeoPandas, reprojected from WGS 84 degrees into metric UTM zones (estimate_utm_crs) to calculate exact square meters, and multiplied by a 65% packing factor (eta = 0.65) to account for 24-foot driving aisles and California Fire Code Title 24 truck access lanes.")
    
    doc.add_heading("3.3 Esri ArcGIS World Imagery Basemap", level=2)
    doc.add_paragraph("High-resolution aerial satellite imagery tiles (256x256 px, Zoom 17, ~1.19 m/pixel) are streamed from Esri's ArcGIS CDN directly beneath the Folium amber canopy overlay, allowing users to see actual asphalt parking stalls and vehicles.")
    
    # ---------------------------------------------------------------------------
    # Section 5
    # ---------------------------------------------------------------------------
    h4 = doc.add_heading("5. Mathematical Modeling & Financial Formulations", level=1)
    h4.paragraph_format.space_before = Pt(14)
    for run in h4.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    doc.add_heading("5.1 System Capacity & Turnkey Cost", level=2)
    add_callout(doc, 
        "P_DC = A_net * 0.20 kW/m2\n"
        "C_total = (P_DC * 1000 * $3.10/W) + (N_chargers * $6,000)",
        title="FORMULA 1: SYSTEM SIZING & TOTAL CAPITAL EXPENDITURE",
        border_color="10B981", bg_color="ECFDF5"
    )
    doc.add_paragraph("Where P_DC is nameplate capacity in kW DC, A_net is active canopy area in m2, $3.10/W reflects commercial carport steel foundations and trenching, and $6,000 covers dual-port Level 2 smart EV charging stations.")
    
    doc.add_heading("5.2 Federal IRA Section 6417 Direct Pay", level=2)
    add_callout(doc, 
        "R_IRA = min(0.30 + beta_domestic + beta_energy + beta_title1, 0.60)\n"
        "C_IRS = C_total * R_IRA\n"
        "C_net = C_total - C_IRS",
        title="FORMULA 2: IRS ELECTIVE DIRECT PAY REIMBURSEMENT",
        border_color="A855F7", bg_color="FAF5FF"
    )
    doc.add_paragraph("Under Section 6417, tax-exempt public school districts receive direct cash reimbursement checks from the IRS via Form 990-T: 30% base credit, +10% domestic steel bonus, +10% energy community bonus, and +10% Title I low-income bonus (capped at 60%).")
    
    doc.add_heading("5.3 Savings, Payback, and 25-Year Lifecycle Cashflow", level=2)
    add_callout(doc, 
        "S_1 = E_AC,annual * Tariff_commercial\n"
        "Payback_years = C_net / S_1\n"
        "E_AC(y) = E_AC,annual * (1 - 0.005)^(y-1)   [PV Degradation: 0.5%/yr]\n"
        "Tariff(y) = Tariff_commercial * (1 + 0.025)^(y-1)   [Rate Escalation: 2.5%/yr]\n"
        "OM(y) = (P_DC * $15.00) * (1 + 0.020)^(y-1)   [Operations & Maintenance]\n"
        "Net_Cashflow(y) = [E_AC(y) * Tariff(y)] - OM(y)\n"
        "Dividend_25 = SUM(y=1 to 25) Net_Cashflow(y) - C_net",
        title="FORMULA 3: 25-YEAR PRO FORMA LIFECYCLE CASHFLOW",
        border_color="F59E0B", bg_color="FFFBEB"
    )
    
    doc.add_heading("5.4 Scope 2 GHG Avoidance", level=2)
    doc.add_paragraph("Annual CO2 reduction = (E_AC,annual * EF_subregion) / 2,204.62 lbs per metric ton. Regional emission factors from EPA eGRID 2024: California CAMX (0.45 lbs CO2/kWh), Texas ERCT (0.85 lbs CO2/kWh), and Midwest RFCW (1.10 lbs CO2/kWh).")
    
    # ---------------------------------------------------------------------------
    # Section 6
    # ---------------------------------------------------------------------------
    h5 = doc.add_heading("6. Software Architecture & File Layout", level=1)
    h5.paragraph_format.space_before = Pt(14)
    for run in h5.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    tree_text = (
        "svyca2026/\n"
        "├── app.py                      # Main Streamlit web application & Folium map\n"
        "├── core/\n"
        "│   ├── __init__.py             # Module namespace\n"
        "│   ├── data_ingest.py          # School database, lot coordinates, and spatial calculations\n"
        "│   ├── solar_engine.py         # NLR PVWatts v8 client, fallback logic, EV synergies\n"
        "│   ├── financial_model.py      # IRA Direct Pay calculations and 25-year cashflows\n"
        "│   └── report_generator.py     # Downloadable 1-page School Board Action Brief\n"
        "├── test_pipeline.py            # Automated end-to-end unit test suite\n"
        "├── requirements.txt            # Python dependencies\n"
        "└── documents/                  # Documentation and pitch guides"
    )
    add_callout(doc, tree_text, title="REPOSITORY STRUCTURE", border_color="64748B", bg_color="F8FAFC")
    
    # ---------------------------------------------------------------------------
    # Section 7
    # ---------------------------------------------------------------------------
    h6 = doc.add_heading("7. Student Defense Guide: Ten Technical Questions & Answers", level=1)
    h6.paragraph_format.space_before = Pt(14)
    for run in h6.runs:
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
    qa_list = [
        ("Q1: What happens under the hood when a school is selected?",
         "data_ingest.py extracts the school's ground-truthed parking lot coordinates and area. The system calculates canopy DC capacity and calls the federal PVWatts v8 API at developer.nlr.gov for AC generation. Simultaneously, financial_model.py computes the IRA Direct Pay check, utility bill savings, and 25-year cashflow, rendering results in Streamlit and Folium."),
        ("Q2: Why developer.nlr.gov instead of developer.nrel.gov?",
         "In May 2026, the Department of Energy transitioned NREL developer services to the National Laboratory of the Rockies (NLR), deprecating the old developer.nrel.gov domain. Our code communicates directly with the active production endpoint."),
        ("Q3: How do you prevent application crashes if network connectivity drops?",
         "solar_engine.py implements an 8-second request timeout and an automated fallback. If the federal server times out or errors, the model draws upon regional irradiance constants from the National Solar Radiation Database (NSRDB) to calculate generation without crashing."),
        ("Q4: Why use a 65% packing factor for parking lots?",
         "Parking lots require 24-foot two-way driving aisles, emergency fire access lanes under California Fire Code Title 24, and curb turning aprons. A 65% ratio represents empirical canopy coverage, calibrated against real installations in Cupertino and Fremont."),
        ("Q5: Canopies cost $3.10/W while rooftops cost $2.20/W. Why choose canopies?",
         "Rooftops carry hidden structural costs: voided roof warranties, HVAC obstructions, and strict seismic load limits. Canopies avoid roof penetrations entirely, lower parking pavement temperatures by 30°F to 45°F, and provide turnkey infrastructure for EV chargers."),
        ("Q6: How do non-taxable public schools receive cash from the IRS?",
         "Under Section 6417 of the Inflation Reduction Act ('Direct Pay') and IRS Treasury Decision 9988, public schools complete an online pre-filing registration and submit IRS Form 990-T with Form 3468. The IRS issues an elective direct cash payment covering 30% to 50% of capital costs."),
        ("Q7: What is the difference between DC capacity and AC generation?",
         "DC capacity (kW DC) is the maximum instantaneous power rating of panels under laboratory sunlight (1,000 W/m² at 25°C). AC generation (kWh AC) is the actual usable energy delivered through the inverter to school switchboards over an entire year after environmental losses."),
        ("Q8: How does the map accurately locate the parking lot?",
         "Campus administrative addresses typically point to main office entrances. We ground-truth exact parking lot asphalt centroids (lot_lat, lot_lon), center the Folium map directly over the lot, and project an amber solar canopy footprint against high-resolution Esri satellite imagery."),
        ("Q9: Why is capital payback faster in California (2.6 yrs) than in Texas (8 yrs)?",
         "Electricity retail tariffs in California exceed $0.34/kWh under PG&E commercial schedules, so every avoided kilowatt-hour produces substantial savings. In Texas, retail electricity averages $0.115/kWh, requiring more years to amortize net capital outlay despite higher solar irradiance."),
        ("Q10: What is the next step for this project?",
         "We plan to distribute this tool to student climate clubs across the Silicon Valley Youth Climate Action network. Students can generate customized Action Briefs and present vetted capital models directly to their local school boards.")
    ]
    
    for q, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        run_q = p_q.add_run(q)
        run_q.bold = True
        run_q.font.name = "Calibri"
        run_q.font.size = Pt(10.5)
        run_q.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        add_callout(doc, a, border_color="3B82F6", bg_color="EFF6FF")
        
    # Save document
    output_path = "DetailedDesignDocument.docx"
    doc.save(output_path)
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    build_word_document()
