"""
generate_pitch_deck.py
Generates an advanced, technically rigorous 16:9 widescreen PowerPoint pitch deck
(SolarSchoolsUSA_PitchDeck.pptx) for Pranav Balaji's presentation at the SVYCA Youth
For Earth Hackathon @ Stanford Climate Week.

Incorporate deep engineering formulations, statutory tax citations, physical loss derate
waterfalls, API contracts, and structural/electrical standards. Zero emojis throughout.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Widescreen Dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette (Stanford Climate Week Tech Aesthetic)
COLOR_BG = RGBColor(9, 13, 22)             # Obsidian Dark Slate (#090D16)
COLOR_CARD = RGBColor(17, 24, 39)          # Card Slate (#111827)
COLOR_CARD_BORDER = RGBColor(31, 41, 61)   # Border Slate (#1F293D)
COLOR_STANFORD = RGBColor(140, 21, 21)     # Stanford Cardinal (#8C1515)
COLOR_SOLAR = RGBColor(56, 189, 248)       # Solar Sky Blue (#38BDF8)
COLOR_GREEN = RGBColor(16, 185, 129)       # Clean Energy Emerald (#10B981)
COLOR_RED = RGBColor(239, 68, 68)          # Alert Red (#EF4444)
COLOR_AMBER = RGBColor(245, 158, 11)       # Amber (#F59E0B)
COLOR_WHITE = RGBColor(243, 244, 246)      # Off-White Text (#F3F4F6)
COLOR_MUTED = RGBColor(156, 163, 175)      # Muted Text (#9CA3AF)
COLOR_SUBTLE = RGBColor(107, 114, 128)     # Subtle Gray (#6B7280)
COLOR_CODE_BG = RGBColor(11, 17, 32)       # Code/Math Background (#0B1120)

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    return bg

def add_header_bar(slide, slide_num, total_slides=10, category="Stanford Climate Week 2026"):
    # Header background
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.55))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = RGBColor(15, 23, 42)
    top_bar.line.fill.background()

    # Stanford Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.12), Inches(2.2), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_STANFORD
    badge.line.fill.background()
    tf_b = badge.text_frame
    tf_b.word_wrap = False
    p_b = tf_b.paragraphs[0]
    p_b.text = "STANFORD CLIMATE WEEK"
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(255, 255, 255)
    p_b.alignment = PP_ALIGN.CENTER

    # Event subtitle text
    tx_box = slide.shapes.add_textbox(Inches(2.85), Inches(0.08), Inches(6.5), Inches(0.4))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = "SVYCA Youth For Earth Hackathon | Systems Architecture & Climate Finance"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_MUTED

    # Slide Counter
    cnt_box = slide.shapes.add_textbox(Inches(11.2), Inches(0.08), Inches(1.6), Inches(0.4))
    tf_c = cnt_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = f"{slide_num:02d} / {total_slides:02d}"
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_SOLAR
    p_c.alignment = PP_ALIGN.RIGHT

    # Progress bar line
    progress_w = (slide_num / total_slides) * SLIDE_WIDTH
    prog_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.54), progress_w, Inches(0.03))
    prog_line.fill.solid()
    prog_line.fill.fore_color.rgb = COLOR_SOLAR
    prog_line.line.fill.background()

def add_slide_titles(slide, tag, title, subtitle):
    box = slide.shapes.add_textbox(Inches(0.6), Inches(0.68), Inches(12.13), Inches(1.1))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_tag = tf.paragraphs[0]
    p_tag.text = tag.upper()
    p_tag.font.size = Pt(9)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_SOLAR

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    p_title.space_before = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = COLOR_MUTED
    p_sub.space_before = Pt(3)

def add_card(slide, left, top, width, height, border_color=COLOR_CARD_BORDER, top_accent_color=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = border_color
    card.line.width = Pt(1)

    if top_accent_color:
        accent = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.05))
        accent.fill.solid()
        accent.fill.fore_color.rgb = top_accent_color
        accent.line.fill.background()

    return card

def add_math_box(slide, left, top, width, height, formula_text, desc_text):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CODE_BG
    card.line.color.rgb = RGBColor(30, 58, 95)
    card.line.width = Pt(1)

    accent = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.05), height)
    accent.fill.solid()
    accent.fill.fore_color.rgb = COLOR_SOLAR
    accent.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.06), width - Inches(0.24), height - Inches(0.12))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = formula_text
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(224, 242, 254)

    if desc_text:
        p2 = tf.add_paragraph()
        p2.text = desc_text
        p2.font.size = Pt(8)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_before = Pt(2)
    return card

def set_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

# =========================================================================
# MAIN PRESENTATION BUILDER
# =========================================================================
def build_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # ---------------------------------------------------------------------
    # SLIDE 1: Title & Engineering Mission
    # ---------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_header_bar(s1, 1, 10)

    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.7), Inches(2.6))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SYSTEMS ARCHITECTURE & CLIMATE FINANCE PITCH"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SOLAR

    p1 = tf1.add_paragraph()
    p1.text = "SolarSchools USA"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(4)

    p2 = tf1.add_paragraph()
    p2.text = "Autonomous Geospatial Pipeline & 26 U.S.C. Section 6417 Financial Engine\nDemocratizing Clean Energy for 100,000+ US Public Campuses"
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_before = Pt(6)

    # Metadata bar
    mb = s1.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.7), Inches(0.5))
    tf_m = mb.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Presenter: Pranav Balaji (Solo Competitor)  |  Event: SVYCA Youth For Earth Hackathon @ Stanford Climate Week  |  October 2026"
    p_m.font.size = Pt(10.5)
    p_m.font.bold = True
    p_m.font.color.rgb = COLOR_WHITE

    # 4 Architecture Pillars
    col_w = Inches(2.8)
    col_y = Inches(4.55)
    col_h = Inches(2.4)
    pillars = [
        ("Geospatial Ingestion", "NCES + OpenStreetMap", "Automated vector extraction with metric UTM CRS reprojection to eliminate spherical distortion.", COLOR_SOLAR),
        ("Physical Simulation", "DOE / NREL PVWatts v8", "Live REST queries to NSRDB solar radiation grid with a 14.0% aggregate loss derate waterfall.", COLOR_SOLAR),
        ("Statutory Capital Model", "IRA Section 6417 Direct Pay", "30% base + 10% Title I + 10% Energy Community uncapped direct cash reimbursement checks.", COLOR_GREEN),
        ("Civic Governance", "1-Click Board Action Brief", "Compiles executive engineering brief, Form 990-T filing guide, and turnkey School Board Resolution.", COLOR_STANFORD)
    ]
    for idx, (tag, title, desc, col) in enumerate(pillars):
        x = Inches(0.6 + idx * 3.1)
        add_card(s1, x, col_y, col_w, col_h, top_accent_color=col)
        tb = s1.shapes.add_textbox(x + Inches(0.15), col_y + Inches(0.12), col_w - Inches(0.3), col_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag.upper()
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(3)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(6)

    set_speaker_notes(s1,
        "[0:00 - 0:25] 'Judges, my name is Pranav Balaji. Across the United States, 100,000 public schools sit on millions of square meters "
        "of unshaded asphalt, while electricity drains $8 billion from education budgets every year. Today I am presenting SolarSchools USA, "
        "an end-to-end computational pipeline that couples OpenStreetMap vector extraction and live NREL PVWatts physics simulation with the "
        "statutory mechanics of Section 6417 of the Internal Revenue Code.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 2: Problem Formulation: Thermodynamics & Capital Barrier
    # ---------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header_bar(s2, 2, 10)
    add_slide_titles(s2, "Problem Formulation", "Spatial Inefficiency & The $8B Utility Drain",
                     "Thermodynamic microclimate heat islands and institutional capital barriers trap 100,000+ public schools.")

    card_w2 = Inches(3.8)
    card_h2 = Inches(5.1)
    card_y2 = Inches(1.9)

    # Card 1: $8B Macroeconomics
    add_card(s2, Inches(0.6), card_y2, card_w2, card_h2, top_accent_color=COLOR_RED)
    tb1 = s2.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(3.4), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "$8.0B / yr"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p = tf1.add_paragraph()
    p.text = "EIA MACROECONOMIC UTILITY DRAIN"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(2)
    p = tf1.add_paragraph()
    p.text = "According to U.S. EIA commercial data, electricity is public K-12 districts' second-largest operating cost after instructional staff salaries.\n\nSchool boards surrender operating revenue to retail monopolies (e.g. PG&E Schedule B-19 at $0.345/kWh)."
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(12)

    # Card 2: Microclimate Thermodynamics
    add_card(s2, Inches(4.766), card_y2, card_w2, card_h2, top_accent_color=COLOR_RED)
    tb2 = s2.shapes.add_textbox(Inches(4.966), Inches(2.05), Inches(3.4), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "+35 to 45°F"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p = tf2.add_paragraph()
    p.text = "ASPHALT ALBEDO DEGRADATION"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(2)
    p = tf2.add_paragraph()
    p.text = "Unshaded asphalt has a solar reflectance albedo of alpha ≈ 0.05–0.10, absorbing direct beam irradiance and elevating pavement temperatures to 145°F.\n\nIdle parking lots act as massive thermal heat sinks across campus microclimates instead of generating clean localized power."
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(12)

    # Card 3: Statutory IRC Barrier
    add_card(s2, Inches(8.933), card_y2, card_w2, card_h2, top_accent_color=COLOR_RED)
    tb3 = s2.shapes.add_textbox(Inches(9.133), Inches(2.05), Inches(3.4), Inches(4.7))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "IRC § 48"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p = tf3.add_paragraph()
    p.text = "PRE-2022 TAX-EXEMPT BARRIER"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(2)
    p = tf3.add_paragraph()
    p.text = "Because school districts are tax-exempt, they could not utilize federal solar tax credits without predatory third-party tax-equity flip leases.\n\nPrivate solar engineering consultants charge $15,000 to $25,000 per feasibility assessment, pricing out suburban, rural, and Title I schools."
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(12)

    set_speaker_notes(s2,
        "[0:25 - 0:50] 'Let's examine the engineering problem. First, thermodynamics: black asphalt parking lots have an albedo of just "
        "0.05 to 0.10, absorbing solar irradiance and elevating surface temperatures above 145 degrees Fahrenheit. Second, financial law: "
        "public school districts are tax-exempt, meaning historically they could not utilize Section 48 Investment Tax Credits without complex, "
        "predatory tax-equity flip structures. And third, private feasibility consultants cost $15,000 to $25,000 per school, pricing out under-resourced districts.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 3: Statutory Catalyst: 26 U.S.C. Section 6417 Direct Pay
    # ---------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header_bar(s3, 3, 10)
    add_slide_titles(s3, "Statutory Clean Energy Policy", "The Legal Game-Changer: 26 U.S.C. Section 6417",
                     "Internal Revenue Code Elective Pay allows tax-exempt school districts to receive direct cash reimbursement checks.")

    # Left: Treasury Decision 9988
    add_card(s3, Inches(0.6), Inches(1.9), Inches(5.8), Inches(5.1), top_accent_color=COLOR_GREEN)
    tb_l3 = s3.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(5.4), Inches(4.8))
    tf_l3 = tb_l3.text_frame
    tf_l3.word_wrap = True
    p = tf_l3.paragraphs[0]
    p.text = "TREASURY DECISION 9988 STATUTORY MECHANICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    p = tf_l3.add_paragraph()
    p.text = "Finalized by the IRS in March 2024, TD 9988 establishes the administrative procedures for tax-exempt political subdivisions:"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(6)

    # Math equation box
    add_math_box(s3, Inches(0.8), Inches(3.0), Inches(5.4), Inches(0.8),
                 "C_net = C_turnkey - (C_turnkey * R_IRA)",
                 "Where R_IRA is the statutory additive direct cash reimbursement rate (30% to 50%).")

    tb_steps = s3.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(5.4), Inches(2.9))
    tf_st = tb_steps.text_frame
    tf_st.word_wrap = True
    steps = [
        ("1. Pre-Filing Registration (Treas. Reg. § 1.6417-5):", "District registers planned solar canopy on IRS portal to obtain a registration number."),
        ("2. Informational Return (26 U.S.C. § 6417(a)):", "District files annual Form 990-T with Form 3468 attached reporting verified capex."),
        ("3. Direct Check Liquidation (26 U.S.C. § 6417(b)):", "U.S. Treasury issues direct electronic deposit or physical check covering 30% to 50% of cost.")
    ]
    for idx, (st_t, st_d) in enumerate(steps):
        p = tf_st.paragraphs[0] if idx == 0 else tf_st.add_paragraph()
        p.text = st_t
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(6) if idx > 0 else Pt(0)
        p2 = tf_st.add_paragraph()
        p2.text = st_d
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED

    # Right: Additive Bonus Stack Table
    add_card(s3, Inches(6.8), Inches(1.9), Inches(5.933), Inches(5.1), top_accent_color=COLOR_SOLAR)
    tb_r3 = s3.shapes.add_textbox(Inches(7.05), Inches(2.05), Inches(5.4), Inches(4.8))
    tf_r3 = tb_r3.text_frame
    tf_r3.word_wrap = True
    p = tf_r3.paragraphs[0]
    p.text = "STATUTORY ADDITIVE BONUS STACK"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    bonus_items = [
        ("Base Direct Pay Rate: 30.0% Cash Check", "Requires compliance with prevailing wage & registered apprenticeship standards (26 U.S.C. § 45(b)(8)).", COLOR_GREEN),
        ("Domestic Content Adder: +10.0% Cash Check", "Requires 100% US structural steel and certified domestic components (26 U.S.C. § 45(b)(9)).", COLOR_SOLAR),
        ("Title I Low-Income Adder: +10.0% Cash Check", "Applies to schools serving >= 40% low-income student populations (26 U.S.C. § 48(e)).", COLOR_GREEN),
        ("Energy Community Adder: +10.0% Cash Check", "Census tracts with brownfields or historical coal mine/plant closures (26 U.S.C. § 48(a)(14)).", COLOR_SOLAR),
        ("Maximum Statutory Reimbursement: Up to 50% - 60%", "Total federal cash check paid directly into the school district treasury.", COLOR_GREEN)
    ]
    for b_t, b_d, col in bonus_items:
        p = tf_r3.add_paragraph()
        p.text = b_t
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_before = Pt(8)
        p2 = tf_r3.add_paragraph()
        p2.text = b_d
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_before = Pt(1)

    set_speaker_notes(s3,
        "[0:50 - 1:15] 'In 2022, Congress passed Section 6417 of the Internal Revenue Code, known as Elective Pay or Direct Pay, "
        "and the IRS finalized Treasury Decision 9988 in March 2024. For the first time in American history, public schools bypass "
        "private tax-equity middlemen: the IRS writes an actual, uncapped direct cash reimbursement check covering 30% to 50% of the turnkey "
        "installation cost. The base rate is 30% for prevailing wage compliance, plus a 10% Title I low-income bonus and 10% domestic content adder. "
        "But over 90% of school boards still do not know this statutory cash check exists.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 4: End-to-End Computational Pipeline & API Architecture
    # ---------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header_bar(s4, 4, 10)
    add_slide_titles(s4, "Software Engineering & Dataflow", "Autonomous 4-Tier Computational Pipeline",
                     "Modularized data ingestion, physical simulation, dynamic discounted cashflow, and civic export in under 3.0s.")

    col_w4 = Inches(2.8)
    col_y4 = Inches(1.9)
    col_h4 = Inches(3.7)

    tiers = [
        ("Tier 1: Geospatial GIS", "Vector Ingestion",
         "NCES & CDE directory lookups. Reprojects angular WGS 84 (EPSG:4326) coordinates into metric UTM zones (gdf.estimate_utm_crs()) to eliminate spherical area distortion.", COLOR_SOLAR),
        ("Tier 2: Physical Engine", "NREL PVWatts v8",
         "Executes live REST queries to NREL API endpoint. Ingests satellite hourly solar irradiance vectors (GHI, DNI, ambient temperature, wind speed from NSRDB).", COLOR_SOLAR),
        ("Tier 3: Financial DCF", "25-Yr Lifecycle Model",
         "Iterates 25-year discounted cashflow integrating 0.5%/yr degradation, 2.5%/yr tariff escalation, 2.0%/yr O&M inflation, and Year 15 inverter reserves.", COLOR_GREEN),
        ("Tier 4: Civic Export", "Action Brief Engine",
         "Compiles board-ready Markdown/PDF brief with executive engineering specs, financial waterfall, and turnkey legal School Board Resolution text.", COLOR_STANFORD)
    ]
    for idx, (t_tag, t_name, t_desc, col) in enumerate(tiers):
        x = Inches(0.6 + idx * 3.1)
        add_card(s4, x, col_y4, col_w4, col_h4, top_accent_color=col)
        tb = s4.shapes.add_textbox(x + Inches(0.15), col_y4 + Inches(0.12), col_w4 - Inches(0.3), col_h4 - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_tag.upper()
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = t_name
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(3)
        p = tf.add_paragraph()
        p.text = t_desc
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(8)

    # Circuit Breaker Fallback Card
    add_card(s4, Inches(0.6), Inches(5.8), Inches(12.133), Inches(1.2), top_accent_color=COLOR_SOLAR)
    tb_fb = s4.shapes.add_textbox(Inches(0.85), Inches(5.88), Inches(11.6), Inches(1.0))
    tf_fb = tb_fb.text_frame
    tf_fb.word_wrap = True
    p = tf_fb.paragraphs[0]
    p.text = "RESILIENT FAULT-TOLERANT CIRCUIT-BREAKER ARCHITECTURE"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p = tf_fb.add_paragraph()
    p.text = "If federal NREL endpoint exceeds an 8.0s timeout, the system executes an automatic fallback to regional NSRDB empirical solar matrices:\nSunbelt: 1,650 kWh/kW-yr  |  Mid-Latitude / CA: 1,460 kWh/kW-yr  |  Northern: 1,320 kWh/kW-yr. The app guarantees zero presentation crashes."
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(3)

    set_speaker_notes(s4,
        "[1:15 - 1:40] 'To bridge this gap, I engineered a 4-tier automated computational pipeline in Python: Tier 1 reprojects WGS 84 "
        "geographic coordinates into metric UTM zones to eliminate spherical distortion and extracts parking polygons. Tier 2 queries the "
        "Department of Energy's NREL PVWatts v8 REST API for satellite solar radiation vectors. Tier 3 computes a 25-year discounted cashflow "
        "integrating degradation, tariff escalation, and O&M reserves. Tier 4 compiles an automated School Board Action Brief. If the federal API "
        "ever times out, our circuit breaker falls back to regional NSRDB solar constants so the system never crashes.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 5: Physics Modeling & NREL Derate Waterfall
    # ---------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header_bar(s5, 5, 10)
    add_slide_titles(s5, "Physical Simulation Engine", "Physics Modeling & NREL Derate Waterfall",
                     "Coupling spatial canopy packing geometry with NREL PVWatts v8 loss algorithms for rigorous yield modeling.")

    # Left: Canopy Packing & API Payload
    add_card(s5, Inches(0.6), Inches(1.9), Inches(5.8), Inches(5.1), top_accent_color=COLOR_SOLAR)
    tb_l5 = s5.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(5.4), Inches(4.8))
    tf_l5 = tb_l5.text_frame
    tf_l5.word_wrap = True
    p = tf_l5.paragraphs[0]
    p.text = "CANOPY SPATIAL PACKING & CAPACITY FORMULATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    add_math_box(s5, Inches(0.8), Inches(2.45), Inches(5.4), Inches(0.9),
                 "A_net = A_gross * eta_packing (eta = 0.65)\nP_DC = A_net * 0.20 kW/m^2 = A_net * 200 W/m^2",
                 "Reserves 24-ft driving aisles & Title 24 fire clearance; assumes 20.0% efficient Mono PERC modules.")

    tb_api = s5.shapes.add_textbox(Inches(0.8), Inches(3.5), Inches(5.4), Inches(3.3))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True
    p = tf_api.paragraphs[0]
    p.text = "NREL PVWatts v8 REST Parameters (core/solar_engine.py):"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    params = [
        ("module_type = 1:", "Premium Monocrystalline PERC silicon (~20% nominal efficiency)."),
        ("array_type = 2:", "Fixed Canopy / Carport structural mounting geometry."),
        ("tilt = 10.0 deg:", "10-degree tilt balancing rainwater shedding, wind loading, and summer insolation."),
        ("azimuth = 180.0 deg:", "True South geographic orientation for optimal North American solar harvesting."),
        ("losses = 14.0%:", "Comprehensive aggregate system derate factor (detailed on right).")
    ]
    for p_k, p_v in params:
        p = tf_api.add_paragraph()
        p.text = f"{p_k} {p_v}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(4)

    # Right: 14.0% Derate Waterfall Table
    add_card(s5, Inches(6.8), Inches(1.9), Inches(5.933), Inches(5.1), top_accent_color=COLOR_SOLAR)
    tb_r5 = s5.shapes.add_textbox(Inches(7.05), Inches(2.05), Inches(5.4), Inches(4.8))
    tf_r5 = tb_r5.text_frame
    tf_r5.word_wrap = True
    p = tf_r5.paragraphs[0]
    p.text = "14.0% AGGREGATE SYSTEM DERATE LOSS WATERFALL"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    derates = [
        ("Inverter Conversion Loss: -4.0%", "Commercial 3-phase string inverters operating at 96.0% CEC weighted efficiency."),
        ("Cell Temperature Derate: -3.0%", "Elevated canopy design provides continuous passive under-panel airflow cooling."),
        ("Soiling & Particulate Dust: -2.5%", "Dry summer dust accumulation; mitigated by annual robotic brush cleaning in O&M."),
        ("DC & AC Ohmic Resistance: -2.0%", "I^2 * R wire losses across underground copper feeders and conduit runs."),
        ("Module Mismatch & Tolerance: -1.5%", "Positive power tolerance binning (+0/+5W) from Tier-1 BloombergNEF manufacturers."),
        ("Diodes & Connection Drops: -1.0%", "MC4 locking connectors and bypass diode voltage drops across series strings."),
        ("Aggregate Derate Factor: 14.0%", "Results in an 86.0% overall System Performance Ratio (PR = 0.86).")
    ]
    for d_t, d_d in derates:
        p = tf_r5.add_paragraph()
        p.text = d_t
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE if "Aggregate" not in d_t else COLOR_GREEN
        p.space_before = Pt(6)
        p2 = tf_r5.add_paragraph()
        p2.text = d_d
        p2.font.size = Pt(8)
        p2.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s5,
        "[1:40 - 2:05] 'Here is our physical modeling rigor. To calculate active solar catchment area, we apply an empirical 65% packing factor "
        "that accounts for 24-foot driving aisles, ADA pathways, and Title 24 fire truck access. System capacity is parameterized at 200 Watts "
        "per square meter for Tier-1 Monocrystalline silicon modules. In NREL PVWatts, we model a fixed 10-degree canopy tilt for optimal rain "
        "drainage and structural wind resistance. Our 14.0% aggregate derate loss waterfall precisely accounts for inverter conversion, module "
        "temperature coefficients, soiling dust, and ohmic wiring resistance.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 6: Empirical Validation (Monta Vista vs Palo Alto)
    # ---------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header_bar(s6, 6, 10)
    add_slide_titles(s6, "Empirical Model Validation", "Ground-Truthed Silicon Valley Case Study",
                     "Calibrating computational simulation against empirical utility data at Monta Vista High vs. quantified delay at Paly.")

    card_w6 = Inches(5.9)
    card_h6 = Inches(5.1)

    # Left: Monta Vista
    add_card(s6, Inches(0.6), Inches(1.9), card_w6, card_h6, top_accent_color=COLOR_GREEN)
    tb_mv = s6.shapes.add_textbox(Inches(0.85), Inches(2.05), card_w6 - Inches(0.5), card_h6 - Inches(0.3))
    tf_mv = tb_mv.text_frame
    tf_mv.word_wrap = True
    p = tf_mv.paragraphs[0]
    p.text = "MONTA VISTA HIGH (IMPLEMENTED LEADER)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    p = tf_mv.add_paragraph()
    p.text = "FUHSD & ENGIE 550 kW Carports (OSM Way 416432160, Lat 37.3151, Lon -122.0581)"
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(1)

    mv_metrics = [
        ("Modeled Nameplate Capacity", "718.2 kW DC (550 kW AC inverter limit)"),
        ("Simulated Annual Generation", "1,484,069 kWh / year"),
        ("Modeled Avoided Bill (PG&E B-19)", "$145,000 / year"),
        ("Empirical District Utility Offset", "$139,200 / year (Published FUHSD Bills)"),
        ("Model Accuracy Tolerance", "4.17% Error (Empirically Validated)")
    ]
    for lbl, val in mv_metrics:
        p = tf_mv.add_paragraph()
        p.text = f"{lbl}: {val}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_WHITE if "Accuracy" not in lbl else COLOR_GREEN
        p.font.bold = True if "Accuracy" in lbl else False
        p.space_before = Pt(7)

    p = tf_mv.add_paragraph()
    p.text = "VALIDATION PROOF: Real-world PG&E billing confirms that our 65% packing factor and NREL PVWatts loss waterfall match commercial utility realities within 4.17%."
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_before = Pt(14)

    # Right: Palo Alto High
    add_card(s6, Inches(6.8), Inches(1.9), card_w6, card_h6, top_accent_color=COLOR_RED)
    tb_pa = s6.shapes.add_textbox(Inches(7.05), Inches(2.05), card_w6 - Inches(0.5), card_h6 - Inches(0.3))
    tf_pa = tb_pa.text_frame
    tf_pa.word_wrap = True
    p = tf_pa.paragraphs[0]
    p.text = "PALO ALTO HIGH (UNSHADED OPPORTUNITY)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    p = tf_pa.add_paragraph()
    p.text = "PAUSD Unshaded Asphalt Lot along Embarcadero Rd (7,200 m² Surface Lot)"
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(1)

    pa_metrics = [
        ("Unshaded Parking Footprint", "7,200 m² (~180 Surface Parking Stalls)"),
        ("Potential Solar Canopy Size", "608.4 kW DC System Capacity"),
        ("Avoidable Utility Bill Surrender", "$140,000 / year (Surrendered to Utility)"),
        ("Unclaimed IRS Direct Pay Check", "$754,416 Cash Check Sitting at U.S. Treasury"),
        ("5-Year Delay Penalty", "$700,000 in Permanent Classroom Budget Losses")
    ]
    for lbl, val in pa_metrics:
        p = tf_pa.add_paragraph()
        p.text = f"{lbl}: {val}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_WHITE if "Delay" not in lbl else COLOR_RED
        p.font.bold = True if "Delay" in lbl else False
        p.space_before = Pt(7)

    p = tf_pa.add_paragraph()
    p.text = "THE COST OF INACTION: Every year PAUSD delays action is $140,000 paid to utility companies instead of funding instructional educators."
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_before = Pt(14)

    set_speaker_notes(s6,
        "[2:05 - 2:35] 'We ground-truthed this physics model against real completed solar carports in Silicon Valley. Look at Monta Vista High "
        "School in Cupertino: Fremont Union High School District built 550 kW of carports in 2021. Our computational engine modeled 1,484,000 kWh "
        "annually and $145,000 in utility savings. Their actual published PG&E utility bill records show $139,200 in avoided bills—an empirical model "
        "accuracy within 4.17%! But just 10 miles away at Palo Alto High School, their massive 7,200 m² parking lot sits unshaded, surrendering "
        "$140,000 every year to utility bills, with an unclaimed $754,000 IRS cash check left at the Treasury.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 7: Capital Engineering & 25-Year Lifecycle DCF
    # ---------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header_bar(s7, 7, 10)
    add_slide_titles(s7, "Financial Engineering & Lifecycle Economics", "Turnkey Economics & 25-Year Lifecycle DCF",
                     "Structural steel canopies require a $3.10/W capex benchmark, but Section 6417 cuts net capex to $1.86/W.")

    card_w7 = Inches(3.8)
    card_h7 = Inches(2.6)
    card_y7 = Inches(1.9)

    c_stats7 = [
        ("$3.10 / W", "COMMERCIAL TURNKEY CAPEX", "Reflects commercial structural steel cantilever columns, CIDH reinforced concrete pier foundations, switchgear, and trench conduit.", COLOR_SOLAR),
        ("-$1.24 / W", "40% IRS DIRECT PAY CHECK", "30% base + 10% Title I or Domestic Content adder paid via direct cash check from U.S. Treasury, bypassing private tax investors.", COLOR_GREEN),
        ("$1.86 / W", "NET DISTRICT CAPITAL OUTLAY", "Net outlay drops to $1.86/W, delivering rapid simple payback within 2.6 to 4.5 years under standard commercial tariffs.", COLOR_GREEN)
    ]
    for idx, (num, lbl, desc, col) in enumerate(c_stats7):
        x = Inches(0.6 + idx * 4.15)
        add_card(s7, x, card_y7, card_w7, card_h7, top_accent_color=col)
        tb = s7.shapes.add_textbox(x + Inches(0.18), card_y7 + Inches(0.12), card_w7 - Inches(0.36), card_h7 - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = lbl
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_SUBTLE
        p.space_before = Pt(2)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(6)

    # Bottom DCF Math Card
    add_card(s7, Inches(0.6), Inches(4.7), Inches(12.133), Inches(2.3), top_accent_color=COLOR_GREEN)
    tb_dcf = s7.shapes.add_textbox(Inches(0.85), Inches(4.8), Inches(11.6), Inches(2.1))
    tf_dcf = tb_dcf.text_frame
    tf_dcf.word_wrap = True
    p = tf_dcf.paragraphs[0]
    p.text = "DYNAMIC 25-YEAR DISCOUNTED CASHFLOW (DCF) FORMULATION"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    add_math_box(s7, Inches(0.85), Inches(5.15), Inches(11.6), Inches(0.9),
                 "D_25 = sum_{y=1}^{25} [ (E_AC * (1 - 0.005)^{y-1} * T_comm * (1 + 0.025)^{y-1}) - (P_DC * $15 * (1 + 0.02)^{y-1}) ] - C_net",
                 "Where y is year, module degradation is 0.5%/yr, tariff escalation is 2.5%/yr, and O&M inflation is 2.0%/yr (with Year 15 inverter replacement reserve).")

    tb_div = s7.shapes.add_textbox(Inches(0.85), Inches(6.15), Inches(11.6), Inches(0.7))
    tf_div = tb_div.text_frame
    tf_div.word_wrap = True
    p = tf_div.paragraphs[0]
    p.text = "Monta Vista High 25-Yr Net Operating Dividend: $14,692,450   |   Palo Alto High 25-Yr Net Operating Dividend: $11,139,946"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    set_speaker_notes(s7,
        "[2:35 - 3:00] 'Our financial model is grounded in commercial capital benchmarks. Structural steel canopies carry a premium of "
        "$3.10 per watt due to cantilever framing and concrete pier foundations. But when you apply the 40% IRS Direct Pay check, net capital "
        "outlay drops to $1.86 per watt. Under standard commercial tariffs, this yields a rapid payback of 2.6 to 4.5 years. Over 25 years—after "
        "budgeting $15 per kilowatt-year for robotic panel washing and full inverter replacement—a single high school generates over $11 million "
        "to $14 million in cumulative net savings back into instructional budgets.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 8: Structural Civil & Electrical Interconnection
    # ---------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header_bar(s8, 8, 10)
    add_slide_titles(s8, "Engineering Specifications", "Structural Steel & Electrical Interconnection",
                     "Engineered to comply with ASCE 7-16 structural codes, California Title 24, and IEEE 1547-2018 standards.")

    card_w8 = Inches(5.9)
    card_h8 = Inches(5.1)

    # Left: Structural Civil
    add_card(s8, Inches(0.6), Inches(1.9), card_w8, card_h8, top_accent_color=COLOR_SOLAR)
    tb_st8 = s8.shapes.add_textbox(Inches(0.85), Inches(2.05), card_w8 - Inches(0.5), card_h8 - Inches(0.3))
    tf_st8 = tb_st8.text_frame
    tf_st8.word_wrap = True
    p = tf_st8.paragraphs[0]
    p.text = "STRUCTURAL CIVIL ENGINEERING SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    struct_items = [
        ("Superstructure Steel:", "ASTM A992 structural wide-flange columns and cold-formed C-channel purlins with hot-dip galvanized coating (ASTM A123)."),
        ("Foundation System:", "Cast-in-drilled-hole (CIDH) reinforced concrete cylindrical piers (30–36 in diameter, 8–12 ft depth) resisting lateral soil overturning."),
        ("Vertical Clearance:", "14.0 ft minimum vertical clearance under lowest purlin to permit school bus and emergency apparatus transit (CA Fire Code Title 24 § 503)."),
        ("Wind & Seismic Rating:", "ASCE 7-16 structural engineering compliance rated for 110 mph basic wind speed and CBC Seismic Design Category D."),
        ("Stormwater Drainage:", "Integrated gutter collectors and internal column downspouts preventing sheet flow across walking aisles.")
    ]
    for s_k, s_v in struct_items:
        p = tf_st8.add_paragraph()
        p.text = s_k
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(6)
        p2 = tf_st8.add_paragraph()
        p2.text = s_v
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED

    # Right: Electrical Interconnection
    add_card(s8, Inches(6.8), Inches(1.9), card_w8, card_h8, top_accent_color=COLOR_BLUE if hasattr(globals(), 'COLOR_BLUE') else COLOR_SOLAR)
    tb_el8 = s8.shapes.add_textbox(Inches(7.05), Inches(2.05), card_w8 - Inches(0.5), card_h8 - Inches(0.3))
    tf_el8 = tb_el8.text_frame
    tf_el8.word_wrap = True
    p = tf_el8.paragraphs[0]
    p.text = "ELECTRICAL & GRID INTERCONNECTION SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    elec_items = [
        ("Interconnection Voltage:", "480V / 277V, 3-Phase, 4-Wire Wye utility distribution interconnection at campus main switchgear (MSB)."),
        ("Smart Inverter Standards:", "IEEE 1547-2018 and California Rule 21 compliant with advanced Volt-VAR and Volt-Watt dynamic grid stabilization functions."),
        ("Underground Feeders:", "Schedule 40 PVC electrical conduit encased in concrete duct bank with 24-inch minimum burial depth under asphalt."),
        ("Fleet Electrification Ready:", "Dedicated 200A 480V distribution subpanel feeding integrated Level 2 EV charging pedestals for staff and overnight fleet charging."),
        ("Telemetry & Monitoring:", "Revenue-grade bidirectional utility interval meter with cellular telemetry transmitting generation data to student science dashboards.")
    ]
    for e_k, e_v in elec_items:
        p = tf_el8.add_paragraph()
        p.text = e_k
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(6)
        p2 = tf_el8.add_paragraph()
        p2.text = e_v
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED

    set_speaker_notes(s8,
        "[3:00 - 3:20] 'From a civil and electrical engineering standpoint: canopies use ASTM A992 structural wide-flange steel columns "
        "anchored in cast-in-drilled-hole reinforced concrete piers, engineered to ASCE 7-16 for 110 mph wind loads. We mandate a 14-foot vertical "
        "clearance for school bus transit. Electrically, systems interconnect at 480V 3-phase commercial switchgear using IEEE 1547 and "
        "California Rule 21 compliant smart inverters that provide Volt-VAR dynamic grid support, with ready conduit for Level 2 EV charging "
        "for teachers and electric school bus fleets.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 9: Scalability Pipeline & Equity Stratification
    # ---------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header_bar(s9, 9, 10)
    add_slide_titles(s9, "Geospatial Expansion & Environmental Justice", "3-Phase Scalability & Environmental Justice",
                     "Structured data architecture scaling from local Silicon Valley calibration to all 100,000+ US public campuses.")

    phases9 = [
        ("Phase 1", "San Francisco Bay Area", "9 Counties & 18 Campuses",
         "Calibrated against active arrays in Cupertino Union (5.2 MW) and Fremont Union High School District under PG&E Schedule B-19.\n\nStatus: Verified & Ground-Truthed", COLOR_SOLAR),
        ("Phase 2", "California Statewide", "58 Counties & 10,000 Schools",
         "Ingests California Department of Education directory. Integrates CalEnviroScreen 4.0 equity scoring, Title 24 solar mandates, and SCE/SDG&E/SMUD commercial utility rates.\n\nStatus: Architecture Specified", COLOR_SOLAR),
        ("Phase 3", "Nationwide USA", "50 States & 100,000+ Schools",
         "Scales via National Center for Education Statistics (NCES) directory, state EIA commercial electricity rates, and EPA eGRID subregion carbon intensity factors.\n\nStatus: National Architecture", COLOR_GREEN)
    ]
    for idx, (p_num, p_name, p_stat, p_desc, col) in enumerate(phases9):
        x = Inches(0.6 + idx * 4.15)
        add_card(s9, x, Inches(1.9), Inches(3.8), Inches(3.6), top_accent_color=col)
        tb = s9.shapes.add_textbox(x + Inches(0.2), Inches(2.05), Inches(3.4), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_num
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = p_name.upper()
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(3)
        p = tf.add_paragraph()
        p.text = p_stat
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_SOLAR
        p.space_before = Pt(3)
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(8)

    # Bottom eGRID Grid Carbon Intensity Card
    add_card(s9, Inches(0.6), Inches(5.7), Inches(12.133), Inches(1.3), top_accent_color=COLOR_GREEN)
    tb_eg = s9.shapes.add_textbox(Inches(0.85), Inches(5.78), Inches(11.6), Inches(1.1))
    tf_eg = tb_eg.text_frame
    tf_eg.word_wrap = True
    p = tf_eg.paragraphs[0]
    p.text = "EPA eGRID REGIONAL GRID CARBON INTENSITY FACTORS (Scope 2 GHG Avoidance)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p = tf_eg.add_paragraph()
    p.text = "CAMX (California / WECC): 0.45 lbs CO2 / kWh  |  ERCOT (Texas): 0.88 lbs CO2 / kWh  |  RFCW (Midwest): 1.12 lbs CO2 / kWh\nKey Environmental Justice Finding: Installing a solar canopy in coal-heavy Midwest grids yields 2.5x higher carbon avoidance per watt than in California."
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(3)

    set_speaker_notes(s9,
        "[3:20 - 3:35] 'Our scalability roadmap expands across three phases: Phase 1 calibrated locally across 9 Bay Area counties under "
        "PG&E B-19. Phase 2 scales across all 10,000 California campuses incorporating CalEnviroScreen 4.0 equity overlays and Title 24 mandates. "
        "Phase 3 scales nationwide across 100,000 campuses using NCES directory data and EPA eGRID regional carbon intensity factors—where Midwest "
        "solar avoids 2.5 times more carbon per watt than in California due to coal grid baseloads.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 10: Civic Synthesis & School Board Resolution Engine
    # ---------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header_bar(s10, 10, 10)
    add_slide_titles(s10, "Civic Implementation & Governance", "Civic Climax: School Board Resolution Engine",
                     "Translating complex engineering and statutory tax law into actionable school board governance.")

    # Left: Action Brief Features
    add_card(s10, Inches(0.6), Inches(1.9), Inches(5.8), Inches(5.1), top_accent_color=COLOR_SOLAR)
    tb_ab10 = s10.shapes.add_textbox(Inches(0.85), Inches(2.05), Inches(5.3), Inches(4.8))
    tf_ab10 = tb_ab10.text_frame
    tf_ab10.word_wrap = True
    p = tf_ab10.paragraphs[0]
    p.text = "AUTOMATED 1-CLICK ACTION BRIEF COMPONENTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    brief_features = [
        ("1. Engineering Specifications:", "System kW DC nameplate, net canopy catchment area (m²), and shaded parking stalls."),
        ("2. Financial Waterfall Schedule:", "Turnkey capex, Section 6417 direct cash reimbursement check, and simple payback years."),
        ("3. Cost of Inaction Matrix:", "Quantified 5-year financial penalty if trustees delay procurement by even a single term."),
        ("4. IRS Statutory Compliance Guide:", "Step-by-step instructions for electronic Pre-Filing Registration and Form 990-T submission."),
        ("5. Template Board Resolution:", "Vote-ready legal language empowering trustees to authorize competitive RFP issuance.")
    ]
    for b_k, b_v in brief_features:
        p = tf_ab10.add_paragraph()
        p.text = b_k
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_SOLAR
        p.space_before = Pt(6)
        p2 = tf_ab10.add_paragraph()
        p2.text = b_v
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED

    # Right: Generated Resolution Language & Closing Call
    add_card(s10, Inches(6.8), Inches(1.9), Inches(5.933), Inches(5.1), top_accent_color=COLOR_STANFORD)
    tb_res = s10.shapes.add_textbox(Inches(7.05), Inches(2.05), Inches(5.4), Inches(4.8))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    p = tf_res.paragraphs[0]
    p.text = "GENERATED BOARD RESOLUTION LANGUAGE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    res_body = (
        "RESOLUTION NO. 2026-SOLAR-01\n"
        "BOARD OF TRUSTEES, PUBLIC SCHOOL DISTRICT\n\n"
        "WHEREAS, the District expends substantial operating funds annually on retail electric utility tariffs; and\n\n"
        "WHEREAS, Section 6417 of the Internal Revenue Code (26 U.S.C. § 6417) provides direct elective cash reimbursement payments from the U.S. Treasury covering 30% to 50% of clean energy canopy installations; and\n\n"
        "NOW, THEREFORE, BE IT RESOLVED that the Board directs the Superintendent to initiate a competitive RFP for parking lot solar carports to capture available federal Direct Pay funds and protect operating budgets."
    )
    p = tf_res.add_paragraph()
    p.text = res_body
    p.font.size = Pt(8)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(6)

    # Final Hero Callout
    p = tf_res.add_paragraph()
    p.text = "EVERY YEAR OF DELAY COSTS A SINGLE HIGH SCHOOL $140,000."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(14)
    p2 = tf_res.add_paragraph()
    p2.text = "Let's shade our parking lots, capture federal funds, and power our classrooms."
    p2.font.size = Pt(9)
    p2.font.color.rgb = COLOR_SOLAR

    set_speaker_notes(s10,
        "[3:35 - 3:50] 'Here is our civic climax: Tab 5 translates all this computational physics into institutional governance. "
        "In one click, students or PTAs generate a complete School Board Action Brief with exact engineering specs, a 25-year cashflow schedule, "
        "IRS Form 990-T filing instructions, and a turnkey School Board Resolution ready for elected trustees to sponsor. Every year of delay costs "
        "a single high school $140,000. Let's shade our parking lots, capture federal funds, and power our classrooms. Thank you!'"
    )

    output_path = "/home/balaji/personal/pranav/svyca2026/SolarSchoolsUSA_PitchDeck.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint deck: {output_path}")

if __name__ == "__main__":
    build_deck()
