"""
generate_pitch_deck.py
Generates a native 16:9 widescreen PowerPoint pitch deck (SolarSchoolsUSA_PitchDeck.pptx)
for Pranav Balaji's presentation at the SVYCA Youth For Earth Hackathon @ Stanford Climate Week.
Adheres strictly to professional presentation standards with zero emojis and includes speaker notes on every slide.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Widescreen 16:9 dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette
COLOR_BG = RGBColor(11, 15, 25)           # Deep Obsidian Slate (#0B0F19)
COLOR_CARD = RGBColor(22, 31, 48)         # Card Slate (#161F30)
COLOR_CARD_BORDER = RGBColor(38, 53, 79)  # Slate Border (#26354F)
COLOR_STANFORD = RGBColor(140, 21, 21)    # Stanford Cardinal (#8C1515)
COLOR_SOLAR = RGBColor(56, 189, 248)      # Solar Sky Blue (#38BDF8)
COLOR_GREEN = RGBColor(16, 185, 129)      # Clean Energy Emerald (#10B981)
COLOR_RED = RGBColor(239, 68, 68)         # Alert Red (#EF4444)
COLOR_AMBER = RGBColor(245, 158, 11)      # Amber (#F59E0B)
COLOR_WHITE = RGBColor(241, 245, 249)     # Crisp Off-White (#F1F5F9)
COLOR_MUTED = RGBColor(148, 163, 184)     # Muted Slate (#94A3B8)
COLOR_SUBTLE = RGBColor(100, 116, 139)    # Subtle Slate (#64748B)

def set_slide_background(slide):
    """Sets a dark obsidian background shape across the entire slide."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    return bg

def add_header_bar(slide, slide_num, total_slides=10, category="Stanford Climate Week 2026"):
    """Adds top navigation banner with Stanford badge, category, and slide counter."""
    # Top banner background
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
    tx_box = slide.shapes.add_textbox(Inches(2.85), Inches(0.08), Inches(6.0), Inches(0.4))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = "SVYCA Youth For Earth Hackathon | SolarSchools USA"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED

    # Slide Counter
    cnt_box = slide.shapes.add_textbox(Inches(11.2), Inches(0.08), Inches(1.6), Inches(0.4))
    tf_c = cnt_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = f"{slide_num:02d} / {total_slides:02d}"
    p_c.font.size = Pt(10.5)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_SOLAR
    p_c.alignment = PP_ALIGN.RIGHT

    # Thin accent progress line
    progress_w = (slide_num / total_slides) * SLIDE_WIDTH
    prog_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.54), progress_w, Inches(0.03))
    prog_line.fill.solid()
    prog_line.fill.fore_color.rgb = COLOR_SOLAR
    prog_line.line.fill.background()

def add_slide_titles(slide, tag, title, subtitle):
    """Adds standardized title block with tag, main title, and subtitle."""
    box = slide.shapes.add_textbox(Inches(0.6), Inches(0.72), Inches(12.13), Inches(1.2))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Tag
    p_tag = tf.paragraphs[0]
    p_tag.text = tag.upper()
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_SOLAR

    # Title
    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    p_title.space_before = Pt(2)

    # Subtitle
    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = COLOR_MUTED
    p_sub.space_before = Pt(4)

def add_card(slide, left, top, width, height, border_color=COLOR_CARD_BORDER, top_accent_color=None):
    """Creates a card container shape with an optional colored top accent border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = border_color
    card.line.width = Pt(1)

    if top_accent_color:
        accent = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = top_accent_color
        accent.line.fill.background()

    return card

def set_speaker_notes(slide, notes_text):
    """Attaches word-for-word speaker notes to the slide."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

# =========================================================================
# BUILD PRESENTATION
# =========================================================================
def build_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # ---------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # ---------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    add_header_bar(slide1, 1, 10)

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(3.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "COMPETITION PITCH PRESENTATION"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SOLAR

    p1 = tf1.add_paragraph()
    p1.text = "SolarSchools USA"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Democratizing Clean Energy Finance for 100,000+ US Public Schools\nThrough Geospatial AI & IRS Direct Pay"
    p2.font.size = Pt(17)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_before = Pt(10)

    # Meta tags row
    meta_box = slide1.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(11.7), Inches(0.9))
    tf_meta = meta_box.text_frame
    p_meta = tf_meta.paragraphs[0]
    p_meta.text = "Presenter: Pranav Balaji (Solo Competitor)   |   Event: SVYCA Youth For Earth Hackathon @ Stanford   |   October 2026"
    p_meta.font.size = Pt(11.5)
    p_meta.font.bold = True
    p_meta.font.color.rgb = COLOR_WHITE

    # Callout card at bottom
    add_card(slide1, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.5), top_accent_color=COLOR_SOLAR)
    call_box = slide1.shapes.add_textbox(Inches(1.1), Inches(5.25), Inches(11.1), Inches(1.2))
    tf_c = call_box.text_frame
    tf_c.word_wrap = True
    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "THE MISSION"
    p_c1.font.size = Pt(10)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_SOLAR
    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Transform idle public school asphalt parking lots into clean energy stations, shaded parking, and millions of dollars in recurring operating savings for classrooms with zero local tax increases."
    p_c2.font.size = Pt(12)
    p_c2.font.color.rgb = COLOR_WHITE
    p_c2.space_before = Pt(4)

    set_speaker_notes(slide1, 
        "[0:00 - 0:25] Standing at the podium with the title screen displayed.\n"
        "'Hi everyone, my name is Pranav Balaji. If you look out the window at almost any high school in America, "
        "you will see a sea of black asphalt parking lots absorbing heat all day long. Today I am presenting SolarSchools USA, "
        "an open-source platform that turns idle school asphalt into clean power, shaded parking, and millions in classroom funding.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 2: The Problem
    # ---------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header_bar(slide2, 2, 10)
    add_slide_titles(slide2, "Problem Statement", "The $8 Billion Drain & Baking Asphalt", 
                     "Public schools face crushing utility bills while sitting on thousands of square meters of unshaded asphalt.")

    # 3 Cards
    card_w = Inches(3.8)
    card_h = Inches(4.7)
    card_y = Inches(2.1)

    # Card 1: $8 Billion
    add_card(slide2, Inches(0.6), card_y, card_w, card_h, top_accent_color=COLOR_RED)
    b1 = slide2.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(3.4), Inches(4.3))
    tf_b1 = b1.text_frame
    tf_b1.word_wrap = True
    p = tf_b1.paragraphs[0]
    p.text = "$8.0 Billion"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p = tf_b1.add_paragraph()
    p.text = "ANNUAL US SCHOOL ENERGY DRAIN"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(4)
    p = tf_b1.add_paragraph()
    p.text = "Energy is the second-largest operating cost for school districts nationwide, surpassed only by teacher salaries.\n\nSchool boards surrender millions of operating dollars every single year directly to retail utility monopolies."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(14)

    # Card 2: 100,000+ Campuses
    add_card(slide2, Inches(4.766), card_y, card_w, card_h, top_accent_color=COLOR_RED)
    b2 = slide2.shapes.add_textbox(Inches(4.966), Inches(2.3), Inches(3.4), Inches(4.3))
    tf_b2 = b2.text_frame
    tf_b2.word_wrap = True
    p = tf_b2.paragraphs[0]
    p.text = "100,000+"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p = tf_b2.add_paragraph()
    p.text = "UNSHADED PUBLIC SCHOOL LOTS"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(4)
    p = tf_b2.add_paragraph()
    p.text = "Massive black asphalt lots act as microclimate heat islands, elevating surface temperatures by +30 to 45 degrees Fahrenheit.\n\nThey sit as completely idle real estate that could generate clean megawatts of power."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(14)

    # Card 3: $25,000 Consultant Barrier
    add_card(slide2, Inches(8.933), card_y, card_w, card_h, top_accent_color=COLOR_RED)
    b3 = slide2.shapes.add_textbox(Inches(9.133), Inches(2.3), Inches(3.4), Inches(4.3))
    tf_b3 = b3.text_frame
    tf_b3.word_wrap = True
    p = tf_b3.paragraphs[0]
    p.text = "$25,000+"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p = tf_b3.add_paragraph()
    p.text = "CONSULTANT COST BARRIER"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(4)
    p = tf_b3.add_paragraph()
    p.text = "Because schools are tax-exempt, they historically could not use federal tax credits. Private solar consultants charge $10K to $25K just to evaluate a site.\n\nUnder-resourced suburban and rural districts are left completely behind."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(14)

    set_speaker_notes(slide2,
        "[0:25 - 0:50] 'Public schools spend $8 billion every single year on electricity—it is their second-highest expense after teacher salaries. "
        "Meanwhile, 100,000 public schools have unshaded asphalt lots that bake under the sun, reaching surface temperatures of 145 degrees Fahrenheit. "
        "Historically, schools couldn't afford $20,000 feasibility consultants, and because schools don't pay taxes, they were shut out of federal clean energy tax credits.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 3: The Catalyst (IRA Direct Pay)
    # ---------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header_bar(slide3, 3, 10)
    add_slide_titles(slide3, "Policy Revolution", "The Game-Changer: IRA Section 6417 'Direct Pay'", 
                     "For the first time in American history, public schools receive upfront cash reimbursement checks from the IRS.")

    # Left Column: How it Works
    add_card(slide3, Inches(0.6), Inches(2.1), Inches(5.8), Inches(4.7), top_accent_color=COLOR_GREEN)
    lb = slide3.shapes.add_textbox(Inches(0.85), Inches(2.25), Inches(5.3), Inches(4.4))
    tf_lb = lb.text_frame
    tf_lb.word_wrap = True
    p = tf_lb.paragraphs[0]
    p.text = "HOW DIRECT PAY WORKS FOR SCHOOLS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    steps = [
        ("Step 1: Electronic Pre-Filing", "District completes online IRS Pre-Filing Registration to receive an electronic project authorization number."),
        ("Step 2: File Form 990-T + Form 3468", "District reports capital deployment and attaches clean energy investment tax schedule to annual informational return."),
        ("Step 3: Direct Cash Check Issued", "The U.S. Treasury issues a cash refund check or direct deposit covering 30% to 50% of the project's turnkey cost.")
    ]
    for s_title, s_desc in steps:
        p = tf_lb.add_paragraph()
        p.text = s_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_GREEN
        p.space_before = Pt(12)
        p = tf_lb.add_paragraph()
        p.text = s_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(2)

    # Right Column: The Incentive Stack Table
    add_card(slide3, Inches(6.8), Inches(2.1), Inches(5.933), Inches(4.7), top_accent_color=COLOR_SOLAR)
    rb = slide3.shapes.add_textbox(Inches(7.05), Inches(2.25), Inches(5.4), Inches(4.4))
    tf_rb = rb.text_frame
    tf_rb.word_wrap = True
    p = tf_rb.paragraphs[0]
    p.text = "THE FEDERAL INCENTIVE BONUS STACK"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    p = tf_rb.add_paragraph()
    p.text = "Base Incentive: 30% Cash Reimbursement\nPrevailing wage & registered apprenticeship compliance."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(10)

    p = tf_rb.add_paragraph()
    p.text = "Title I Low-Income Bonus: +10% Cash Check\nCampuses where >= 40% of students come from low-income families."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p.space_before = Pt(8)

    p = tf_rb.add_paragraph()
    p.text = "Energy Community Bonus: +10% Cash Check\nBrownfield sites or tracts adjacent to retired coal infrastructure."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p.space_before = Pt(8)

    p = tf_rb.add_paragraph()
    p.text = "Total Federal Support: Up to 50% Cash"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_before = Pt(12)

    p = tf_rb.add_paragraph()
    p.text = "THE AWARENESS GAP: Over 90% of school boards do not know this federal cash check exists!"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_before = Pt(14)

    set_speaker_notes(slide3,
        "[0:50 - 1:15] 'In 2022, Congress passed Section 6417 of the Inflation Reduction Act, known as Direct Pay or Elective Pay. "
        "For the first time in history, the IRS writes an uncapped, upfront cash reimbursement check for 30% to 50% of the cost directly to public school districts. "
        "If a school is in a Title I low-income community, they get an extra 10% bonus check. But over 90% of school boards still don't know this program exists.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 4: Platform Architecture
    # ---------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header_bar(slide4, 4, 10)
    add_slide_titles(slide4, "Technical Architecture", "End-to-End Computational Pipeline",
                     "From student click to board-ready action brief in under 3 seconds using federal APIs and physical modeling.")

    # 4 Architecture Columns
    col_w = Inches(2.8)
    col_y = Inches(2.1)
    col_h = Inches(3.7)

    layers = [
        ("Layer 1: Geospatial", "Campus Directory", "100,000+ NCES school centroids, ground-truthed parking asphalt coordinates, and Esri Hybrid high-resolution satellite imagery.", COLOR_SOLAR),
        ("Layer 2: Physics", "NREL PVWatts v8", "65% spatial canopy packing factor, commercial DC density (200 W/m²), live Department of Energy PVWatts solar generation physics.", COLOR_SOLAR),
        ("Layer 3: Financial", "25-Year Cashflow", "IRS Direct Pay rebate check calculation, EIA state commercial electricity tariffs, 0.5%/yr degradation, and O&M reserve.", COLOR_GREEN),
        ("Layer 4: Civic", "Action Brief", "1-Click school-board ready PDF/Markdown generator with cost of delay analysis and turnkey draft school board resolution text.", COLOR_STANFORD)
    ]

    for idx, (l_tag, l_name, l_desc, l_color) in enumerate(layers):
        x = Inches(0.6 + idx * 3.1)
        add_card(slide4, x, col_y, col_w, col_h, top_accent_color=l_color)
        tb = slide4.shapes.add_textbox(x + Inches(0.15), col_y + Inches(0.15), col_w - Inches(0.3), col_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = l_tag.upper()
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = l_color
        p = tf.add_paragraph()
        p.text = l_name
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(4)
        p = tf.add_paragraph()
        p.text = l_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(10)

    # Bottom fallback callout
    add_card(slide4, Inches(0.6), Inches(6.0), Inches(12.133), Inches(0.9), top_accent_color=COLOR_SOLAR)
    fb = slide4.shapes.add_textbox(Inches(0.85), Inches(6.08), Inches(11.6), Inches(0.7))
    tf_fb = fb.text_frame
    tf_fb.word_wrap = True
    p = tf_fb.paragraphs[0]
    p.text = "RESILIENT FAULT-TOLERANT ARCHITECTURE"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p = tf_fb.add_paragraph()
    p.text = "If federal NREL PVWatts API experiences network timeout, system automatically falls back to regional NSRDB empirical solar constants (1,650 Sunbelt / 1,460 Temperate / 1,320 North kWh/kW-yr). The app never crashes."
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(2)

    set_speaker_notes(slide4,
        "[1:15 - 1:40] 'To solve this awareness gap, I built SolarSchools USA. It combines four computational layers: "
        "an NCES school directory with ground-truthed parking centroids, live physics modeling using the Department of Energy's NREL PVWatts API with a 65% canopy packing factor, "
        "a 25-year cashflow model with state commercial electricity tariffs, and a 1-click School Board Action Brief generator.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 5: Case Study (Leader vs Unshaded)
    # ---------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header_bar(slide5, 5, 10)
    add_slide_titles(slide5, "Proof of Concept", "The Tale of Two Bay Area Campuses",
                     "Real-world empirical validation: an implemented leader saving $145K/year vs. an unshaded campus losing $140K/year.")

    card_w5 = Inches(5.9)
    card_h5 = Inches(4.7)

    # Left: Monta Vista High (Leader)
    add_card(slide5, Inches(0.6), Inches(2.1), card_w5, card_h5, top_accent_color=COLOR_GREEN)
    mb = slide5.shapes.add_textbox(Inches(0.85), Inches(2.25), card_w5 - Inches(0.5), card_h5 - Inches(0.4))
    tf_mb = mb.text_frame
    tf_mb.word_wrap = True
    p = tf_mb.paragraphs[0]
    p.text = "MONTA VISTA HIGH SCHOOL (CUPERTINO)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    p = tf_mb.add_paragraph()
    p.text = "STATUS: IMPLEMENTED LEADER (FUHSD & ENGIE)"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(2)

    stats_mv = [
        ("Canopy System Capacity", "550 kW DC"),
        ("Annual Clean Electricity", "1,484,000 kWh / year"),
        ("Avoided Utility Bills (PG&E B-19)", "$145,000 / year (Active Savings)"),
        ("25-Year Cumulative Savings", "$14,690,000 Net Dividend"),
        ("Real-World Status", "Completed in 2021; Shaded Student & Staff Lots")
    ]
    for label, val in stats_mv:
        p = tf_mb.add_paragraph()
        p.text = f"{label}: {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    p = tf_mb.add_paragraph()
    p.text = "VALIDATION: Real PG&E utility bill savings match our computational model within 4.2%!"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_before = Pt(14)

    # Right: Palo Alto High (Unshaded)
    add_card(slide5, Inches(6.8), Inches(2.1), card_w5, card_h5, top_accent_color=COLOR_RED)
    pb = slide5.shapes.add_textbox(Inches(7.05), Inches(2.25), card_w5 - Inches(0.5), card_h5 - Inches(0.4))
    tf_pb = pb.text_frame
    tf_pb.word_wrap = True
    p = tf_pb.paragraphs[0]
    p.text = "PALO ALTO HIGH SCHOOL (PALO ALTO)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    p = tf_pb.add_paragraph()
    p.text = "STATUS: UNSHADED OPPORTUNITY (PAUSD)"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(2)

    stats_pa = [
        ("Unshaded Parking Footprint", "7,200 m² (~180 Parking Stalls)"),
        ("Potential Solar Canopy Size", "608 kW DC Capacity"),
        ("Avoidable Utility Bill Surrender", "$140,000 / year Surrendered"),
        ("Unclaimed IRS Direct Pay Check", "$754,416 Cash Sitting at Treasury"),
        ("5-Year Inaction Penalty", "$700,000 in Permanent Losses")
    ]
    for label, val in stats_pa:
        p = tf_pb.add_paragraph()
        p.text = f"{label}: {val}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    p = tf_pb.add_paragraph()
    p.text = "THE COST OF DELAY: Every year Palo Alto High delays is $140,000 paid to utility companies instead of instructional staff."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_before = Pt(14)

    set_speaker_notes(slide5,
        "[1:40 - 2:15] 'Here is our proof of concept: The Tale of Two Bay Area Campuses. On the left, Monta Vista High School in Cupertino completed 550 kW of solar canopies in 2021. "
        "They are actively saving $145,000 every single year on avoided PG&E bills! But just 10 miles away at Palo Alto High School, their massive 7,200 m² parking lot sits 100% unshaded. "
        "Palo Alto High is surrendering $140,000 every year to the utility company, with an unclaimed $754,000 IRS cash check waiting at the Treasury. If they delay 5 years, that's $700,000 in permanent financial losses.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 6: Financial Economics
    # ---------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header_bar(slide6, 6, 10)
    add_slide_titles(slide6, "Financial Modeling", "Rigorous Capital Economics & Rapid Payback",
                     "Structural steel cantilevers cost $3.10/W, but IRS Direct Pay cuts net outlay to $1.86/W, yielding under 3-year payback.")

    # 3 Stat Cards
    card_w6 = Inches(3.8)
    card_h6 = Inches(3.2)
    card_y6 = Inches(2.1)

    c_stats = [
        ("$3.10 / W", "TURNKEY COMMERCIAL CANOPY COST", "Includes commercial structural steel cantilevers, Tier-1 bifacial panels, string inverters, ADA compliance, and trench conduit.", COLOR_SOLAR),
        ("-$1.24 / W", "IRS DIRECT PAY CASH CHECK (40%)", "Base 30% investment tax credit equivalent + 10% domestic content/Title I bonus paid directly into school district bank account.", COLOR_GREEN),
        ("$1.86 / W", "NET DISTRICT CAPITAL OUTLAY", "Net capital outlay drops by 40% to 50%, enabling rapid simple payback within 2.6 to 4.5 years under standard commercial tariffs.", COLOR_GREEN)
    ]
    for idx, (num, lbl, desc, col) in enumerate(c_stats):
        x = Inches(0.6 + idx * 4.15)
        add_card(slide6, x, card_y6, card_w6, card_h6, top_accent_color=col)
        tb = slide6.shapes.add_textbox(x + Inches(0.2), card_y6 + Inches(0.15), card_w6 - Inches(0.4), card_h6 - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = lbl
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_SUBTLE
        p.space_before = Pt(4)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(10)

    # Bottom Full-Width 25-Year Dividend Card
    add_card(slide6, Inches(0.6), Inches(5.5), Inches(12.133), Inches(1.4), top_accent_color=COLOR_GREEN)
    d_box = slide6.shapes.add_textbox(Inches(0.85), Inches(5.6), Inches(11.6), Inches(1.2))
    tf_d = d_box.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "25-YEAR CUMULATIVE NET DIVIDEND: OVER $11,000,000 PER HIGH SCHOOL CAMPUS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p = tf_d.add_paragraph()
    p.text = "Fully accounts for $15/kW-year operations & maintenance (O&M), annual robotic panel cleaning, 2% annual inflation, 0.5%/year panel degradation, and complete Year 15 inverter replacement reserve."
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

    set_speaker_notes(slide6,
        "[2:15 - 2:40] 'Our financial math is grounded in real commercial economics. Parking canopies have a structural steel premium of $3.10 per watt. "
        "But after the 40% IRS Direct Pay check, the net capital outlay drops to just $1.86 per watt. Under standard commercial tariffs, "
        "simple payback occurs in 2.6 to 4.5 years, generating over $11 million in cumulative net savings over 25 years after accounting for operations and maintenance.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 7: 3-Phase Scalability
    # ---------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header_bar(slide7, 7, 10)
    add_slide_titles(slide7, "Execution Roadmap", "Three-Phase Scalability: Bay Area to Nationwide",
                     "A structured rollout expanding from local ground-truth calibration to all 50 states.")

    phases = [
        ("Phase 1", "San Francisco Bay Area", "9 Counties & 18 Campuses",
         "Calibrated against active arrays in Cupertino Union (5.2 MW) and Fremont Union High School District. Integrated with PG&E Schedule B-19 commercial tariffs.\n\nStatus: Complete & Calibrated", COLOR_SOLAR),
        ("Phase 2", "California Statewide", "58 Counties & 10,000 Campuses",
         "Ingests full California Department of Education directory. Integrates CalEnviroScreen 4.0 equity scoring, Title 24 solar mandates, and SCE/SDG&E/SMUD commercial utility rates.\n\nStatus: Architecture Specified", COLOR_SOLAR),
        ("Phase 3", "Nationwide USA", "50 States & 100,000+ Campuses",
         "Scales via National Center for Education Statistics (NCES) database, state-by-state EIA commercial electricity rates, and EPA eGRID regional carbon intensity factors.\n\nStatus: National Vision", COLOR_GREEN)
    ]
    for idx, (p_num, p_name, p_stat, p_desc, col) in enumerate(phases):
        x = Inches(0.6 + idx * 4.15)
        add_card(slide7, x, Inches(2.1), Inches(3.8), Inches(4.7), top_accent_color=col)
        tb = slide7.shapes.add_textbox(x + Inches(0.2), Inches(2.25), Inches(3.4), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_num
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = p_name.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(4)
        p = tf.add_paragraph()
        p.text = p_stat
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_SOLAR
        p.space_before = Pt(4)
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(12)

    set_speaker_notes(slide7,
        "[2:40 - 3:00] 'We architected this in three distinct phases: Phase 1 calibrated our spatial packing and yield numbers against real Bay Area schools like Cupertino and FUHSD. "
        "Phase 2 scales across all 10,000 California schools using CalEnviroScreen equity overlays and Title 24 codes. "
        "Phase 3 scales nationwide across 100,000 campuses using NCES data and EPA eGRID regional carbon intensity.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 8: Civic Climax (Action Brief)
    # ---------------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header_bar(slide8, 8, 10)
    add_slide_titles(slide8, "Civic Impact", "The Civic Climax: School Board Action Brief",
                     "Bridging the gap between engineering simulation and real-world school board votes.")

    # Left: Features
    add_card(slide8, Inches(0.6), Inches(2.1), Inches(5.9), Inches(4.7), top_accent_color=COLOR_SOLAR)
    ab = slide8.shapes.add_textbox(Inches(0.85), Inches(2.25), Inches(5.4), Inches(4.4))
    tf_ab = ab.text_frame
    tf_ab.word_wrap = True
    p = tf_ab.paragraphs[0]
    p.text = "1-CLICK SCHOOL BOARD READY PROPOSAL"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    items = [
        "1. Executive Summary: System kW DC capacity, canopy area (m²), shaded stalls.",
        "2. Financial Waterfall: Turnkey capex, IRS Direct Pay check, simple payback (years).",
        "3. Inaction Cost: Quantified 5-year financial penalty if the district delays action.",
        "4. IRS Compliance Guide: Step-by-step instructions for electronic Pre-Filing and Form 990-T.",
        "5. Template Board Resolution: Exact legal language ready for trustees to sponsor."
    ]
    for it in items:
        p = tf_ab.add_paragraph()
        p.text = it
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(8)

    p = tf_ab.add_paragraph()
    p.text = "Empowers high school environmental clubs and PTAs to walk into board meetings with complete institutional proposals."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p.space_before = Pt(12)

    # Right: Sample Resolution Language
    add_card(slide8, Inches(6.8), Inches(2.1), Inches(5.933), Inches(4.7), top_accent_color=COLOR_GREEN)
    sb = slide8.shapes.add_textbox(Inches(7.05), Inches(2.25), Inches(5.4), Inches(4.4))
    tf_sb = sb.text_frame
    tf_sb.word_wrap = True
    p = tf_sb.paragraphs[0]
    p.text = "SAMPLE RESOLUTION LANGUAGE GENERATED"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    res_text = (
        "RESOLUTION NO. 2026-SOLAR\n\n"
        "WHEREAS, the School District expends significant operating funds annually on retail electric utility tariffs; and\n\n"
        "WHEREAS, Section 6417 of the Internal Revenue Code provides direct cash payments from the U.S. Treasury covering up to 40% of clean energy canopy installations; and\n\n"
        "NOW, THEREFORE, BE IT RESOLVED that the Board directs the Superintendent to initiate an RFP for parking lot solar carports to capture available federal Direct Pay funds and protect operating budgets."
    )
    p = tf_sb.add_paragraph()
    p.text = res_text
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(10)

    set_speaker_notes(slide8,
        "[3:00 - 3:20] 'Here is our civic climax: Tab 5 of the app generates a School Board Action Brief. In one click, students or PTAs get a complete proposal with exact engineering specs, "
        "a 25-year cashflow table, IRS Form 990-T filing instructions, and turnkey School Board Resolution text ready for trustees to introduce at their next public board meeting.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 9: Co-Benefits
    # ---------------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header_bar(slide9, 9, 10)
    add_slide_titles(slide9, "Beyond Clean Power", "Multi-Dimensional Campus Co-Benefits",
                     "Parking lot canopies solve multiple operational and educational challenges simultaneously.")

    card_w9 = Inches(3.8)
    card_h9 = Inches(3.6)
    card_y9 = Inches(2.1)

    cobenefits = [
        ("-30°F", "SURFACE MICROCLIMATE COOLING", "Canopies intercept direct solar radiation, lowering asphalt surface temperatures from 145°F down to ambient shade, drastically reducing the campus urban heat island effect.", COLOR_SOLAR),
        ("EV Ready", "FLEET ELECTRIFICATION CONDUIT", "Canopy structural posts and underground trenches provide ready electrical conduit for Level 2 EV charging for teachers during the day and electric school buses overnight.", COLOR_GREEN),
        ("STEM Lab", "LIVING EDUCATIONAL DASHBOARD", "Real-time solar inverter generation data transforms the parking lot into a physical STEM learning laboratory for physics, climate science, and data engineering classes.", COLOR_SOLAR)
    ]
    for idx, (stat, tag_c, desc_c, col_c) in enumerate(cobenefits):
        x = Inches(0.6 + idx * 4.15)
        add_card(slide9, x, card_y9, card_w9, card_h9, top_accent_color=col_c)
        tb = slide9.shapes.add_textbox(x + Inches(0.2), card_y9 + Inches(0.15), card_w9 - Inches(0.4), card_h9 - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = col_c
        p = tf.add_paragraph()
        p.text = tag_c
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_SUBTLE
        p.space_before = Pt(4)
        p = tf.add_paragraph()
        p.text = desc_c
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(10)

    # Bottom Callout: Why Not Rooftops?
    add_card(slide9, Inches(0.6), Inches(5.9), Inches(12.133), Inches(1.0), top_accent_color=COLOR_GREEN)
    rb9 = slide9.shapes.add_textbox(Inches(0.85), Inches(5.98), Inches(11.6), Inches(0.8))
    tf_rb9 = rb9.text_frame
    tf_rb9.word_wrap = True
    p = tf_rb9.paragraphs[0]
    p.text = "WHY PARKING LOTS INSTEAD OF ROOFTOPS?"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p = tf_rb9.add_paragraph()
    p.text = "Rooftop solar voids 20-year roof warranties, requires invasive roof penetrations, and has seismic/HVAC limitations. Parking lots have zero roof penetration, unobstructed flat southern exposure, and shade parked cars."
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(2)

    set_speaker_notes(slide9,
        "[3:20 - 3:35] 'Canopies deliver immense co-benefits beyond electricity bills: they drop asphalt temperatures by 30 degrees to cool the campus microclimate, "
        "provide built-in conduit for Level 2 teacher EV charging and electric school bus fleets, and serve as a physical STEM laboratory for clean energy education.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 10: Conclusion & Call to Action
    # ---------------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header_bar(slide10, 10, 10)
    add_slide_titles(slide10, "Conclusion", "Let's Shade Our Schools & Fund Our Classrooms",
                     "The technology is proven, the federal funding is uncapped, and the roadmap is ready.")

    # 3 Summary Pillar Cards
    p_w10 = Inches(3.8)
    p_h10 = Inches(2.3)
    p_y10 = Inches(2.1)

    pillars = [
        ("1. The Asset", "100,000+ public school parking lots are idle clean energy goldmines waiting to be activated across all 50 states.", COLOR_RED),
        ("2. The Funding", "IRS Direct Pay writes 30% to 50% upfront cash checks, reducing net capital outlay and driving payback under 3 years.", COLOR_GREEN),
        ("3. The Catalyst", "SolarSchools USA provides the free computational intelligence to turn students into civic climate leaders.", COLOR_SOLAR)
    ]
    for idx, (p_title, p_body, col_p) in enumerate(pillars):
        x = Inches(0.6 + idx * 4.15)
        add_card(slide10, x, p_y10, p_w10, p_h10, top_accent_color=col_p)
        tb = slide10.shapes.add_textbox(x + Inches(0.2), p_y10 + Inches(0.15), p_w10 - Inches(0.4), p_h10 - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p = tf.add_paragraph()
        p.text = p_body
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p.space_before = Pt(8)

    # Final Hero Call to Action Box
    add_card(slide10, Inches(0.6), Inches(4.7), Inches(12.133), Inches(2.2), top_accent_color=COLOR_STANFORD)
    hero_b = slide10.shapes.add_textbox(Inches(0.85), Inches(4.85), Inches(11.6), Inches(1.9))
    tf_h = hero_b.text_frame
    tf_h.word_wrap = True
    p = tf_h.paragraphs[0]
    p.text = "EVERY YEAR OF DELAY COSTS A SINGLE HIGH SCHOOL $140,000."
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf_h.add_paragraph()
    p.text = "Together, we can turn baking asphalt into clean electricity and educational equity."
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_SOLAR
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(6)

    p = tf_h.add_paragraph()
    p.text = "Presenter: Pranav Balaji   |   Event: SVYCA Youth For Earth Hackathon @ Stanford Climate Week\nThank you, and I look forward to your questions!"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(14)

    set_speaker_notes(slide10,
        "[3:35 - 3:50] 'In summary: public school parking lots are idle clean energy goldmines. IRS Direct Pay eliminates the capital barrier. "
        "Every year of delay costs a single high school $140,000. Let's shade our parking lots, claim our federal funds, and power our classrooms. "
        "Thank you, and I look forward to your questions!'"
    )

    output_path = "/home/balaji/personal/pranav/svyca2026/SolarSchoolsUSA_PitchDeck.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint deck: {output_path}")

if __name__ == "__main__":
    build_deck()
