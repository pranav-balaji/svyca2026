"""
generate_pitch_deck.py
Generates a clean, visual, high-impact 16:9 widescreen PowerPoint pitch deck
(SolarSchoolsUSA_PitchDeck.pptx) designed specifically for a 10th-grade presenter
(Pranav Balaji) at the SVYCA Youth For Earth Hackathon @ Stanford Climate Week.

Design Principles:
- Authentic student voice (relatable, passionate, clear).
- Low word count: big numbers, punchy 3-5 word bullet points, zero walls of text.
- Clean modern cards with high contrast.
- Complete speaker notes with a natural, conversational script.
- Zero emojis throughout.
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

# Modern Color Palette
COLOR_BG = RGBColor(11, 15, 25)              # Deep Navy Slate (#0B0F19)
COLOR_CARD = RGBColor(19, 26, 43)           # Card Background (#131A2B)
COLOR_CARD_BORDER = RGBColor(34, 46, 74)    # Subtle Border (#222E4A)
COLOR_STANFORD = RGBColor(140, 21, 21)      # Stanford Cardinal (#8C1515)
COLOR_SOLAR = RGBColor(56, 189, 248)        # Solar Sky Blue (#38BDF8)
COLOR_GREEN = RGBColor(16, 185, 129)        # Emerald Green (#10B981)
COLOR_AMBER = RGBColor(245, 158, 11)        # Warm Amber (#F59E0B)
COLOR_RED = RGBColor(239, 68, 68)           # Coral Red (#EF4444)
COLOR_WHITE = RGBColor(248, 250, 252)       # Crisp White (#F8FAFC)
COLOR_MUTED = RGBColor(160, 174, 192)       # Light Slate (#A0AEC0)
COLOR_SUBTLE = RGBColor(113, 128, 150)      # Muted Label (#718096)

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    return bg

def add_header_bar(slide, slide_num, total_slides=10):
    # Top bar background
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.55))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = RGBColor(15, 23, 42)
    top_bar.line.fill.background()

    # Stanford Pill Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.12), Inches(2.2), Inches(0.32))
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

    # Event context subtitle
    tx_box = slide.shapes.add_textbox(Inches(2.95), Inches(0.08), Inches(6.5), Inches(0.4))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = "SVYCA Youth For Earth Hackathon  |  Clean Energy & School Climate Action"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_MUTED

    # Slide Number
    cnt_box = slide.shapes.add_textbox(Inches(11.2), Inches(0.08), Inches(1.5), Inches(0.4))
    tf_c = cnt_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = f"{slide_num:02d} / {total_slides:02d}"
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_SOLAR
    p_c.alignment = PP_ALIGN.RIGHT

    # Slim Progress line
    progress_w = (slide_num / total_slides) * SLIDE_WIDTH
    prog_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.54), progress_w, Inches(0.025))
    prog_line.fill.solid()
    prog_line.fill.fore_color.rgb = COLOR_SOLAR
    prog_line.line.fill.background()

def add_slide_header(slide, tag, title, subtitle):
    box = slide.shapes.add_textbox(Inches(0.6), Inches(0.68), Inches(12.13), Inches(1.15))
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
    p_title.font.size = Pt(22)
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
        accent = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = top_accent_color
        accent.line.fill.background()

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
    # SLIDE 1: Title & Hook
    # ---------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_header_bar(s1, 1, 10)

    # Title box
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(2.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SVYCA YOUTH FOR EARTH HACKATHON"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SOLAR

    p1 = tf1.add_paragraph()
    p1.text = "SolarSchools USA"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(4)

    p2 = tf1.add_paragraph()
    p2.text = "Turning School Parking Lots into Clean Energy & Classroom Cash"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_GREEN
    p2.space_before = Pt(4)

    p3 = tf1.add_paragraph()
    p3.text = "A simple platform helping students, teachers, and school boards claim federal solar funding in seconds."
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = Pt(6)

    # Presenter bio line
    mb = s1.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.7), Inches(0.45))
    tf_m = mb.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Pranav Balaji  |  10th Grade  |  Silicon Valley Youth Climate Action (SVYCA)  |  October 2026"
    p_m.font.size = Pt(11)
    p_m.font.bold = True
    p_m.font.color.rgb = COLOR_WHITE

    # 3 High-Impact Pillars
    col_w = Inches(3.8)
    col_y = Inches(4.55)
    col_h = Inches(2.4)
    pillars = [
        ("18 Local Schools Mapped", "High-Resolution Campus Data",
         ["High, Middle & Elementary schools mapped", "Exact parking lots ground-truthed on satellite", "Zero manual measuring needed"], COLOR_SOLAR),
        ("Real Solar Physics (NREL)", "Department of Energy Engine",
         ["Uses official PVWatts v8 solar calculations", "Calculates monthly power generation", "Calibrated against active Silicon Valley arrays"], COLOR_GREEN),
        ("1-Click School Board Brief", "Instant Action for Students",
         ["Generates 1-page financial summary", "Includes ready-to-vote board resolution", "Gives students the tools to speak to trustees"], COLOR_STANFORD)
    ]
    for idx, (tag, title, bullets, col) in enumerate(pillars):
        x = Inches(0.6 + idx * 4.15)
        add_card(s1, x, col_y, col_w, col_h, top_accent_color=col)
        tb = s1.shapes.add_textbox(x + Inches(0.2), col_y + Inches(0.12), col_w - Inches(0.4), col_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag.upper()
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(3)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(3)

    set_speaker_notes(s1,
        "[0:00 - 0:25] 'Hi everyone, my name is Pranav Balaji, and I am a 10th grader. "
        "Every single morning when we arrive at school, our parking lots sit empty under the blazing sun. "
        "At the same time, our school districts spend millions of dollars every year on electric bills. "
        "Today I want to show you SolarSchools USA: a web platform I built so any student or school board member "
        "can map their school parking lot, calculate solar energy, and download a ready-to-use board proposal in just 10 seconds.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 2: The Problem: Hot Asphalt & Wasted Budgets
    # ---------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header_bar(s2, 2, 10)
    add_slide_header(s2, "The Real Problem", "Our Parking Lots Are Baking. Our Schools Are Bleeding Cash.",
                     "Millions of square feet of black asphalt are absorbing heat and draining school budgets.")

    card_w2 = Inches(3.8)
    card_h2 = Inches(4.0)
    card_y2 = Inches(1.9)

    cards_s2 = [
        ("140°F", "BLAZING ASPHALT", COLOR_RED, [
            "Empty blacktop bakes student and staff cars",
            "Creates campus heat islands in hot months",
            "Playground asphalt gets too hot to use safely"
        ]),
        ("$8.0 Billion", "WASTED POWER BILLS", COLOR_RED, [
            "Schools spend more on electricity than supplies",
            "Money flows straight to monopoly power companies",
            "Funds that could hire teachers are lost every year"
        ]),
        ("$25,000", "THE CONSULTANT WALL", COLOR_RED, [
            "Engineering feasibility studies cost thousands",
            "Takes 6 to 12 months just to get an estimate",
            "Leaves under-resourced schools completely locked out"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(cards_s2):
        x = Inches(0.6 + idx * 4.15)
        add_card(s2, x, card_y2, card_w2, card_h2, top_accent_color=col)
        tb = s2.shapes.add_textbox(x + Inches(0.2), card_y2 + Inches(0.18), card_w2 - Inches(0.4), card_h2 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(38)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom Callout Card
    add_card(s2, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_RED)
    tb_bot2 = s2.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b2 = tb_bot2.text_frame
    tf_b2.word_wrap = True
    p = tf_b2.paragraphs[0]
    p.text = "THE BOTTOM LINE FOR STUDENTS"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p2 = tf_b2.add_paragraph()
    p2.text = "Every dollar our school district pays to utility companies is a dollar taken away from teachers, arts, and classrooms."
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s2,
        "[0:25 - 0:50] 'Think about what school feels like in August or September. "
        "Our parking lots are black asphalt that reaches 140 degrees. Cars turn into ovens, and playgrounds bake. "
        "Meanwhile, public schools across the country spend over 8 billion dollars every year on electric bills. "
        "Electricity is the second-largest bill a school district pays, right after teacher salaries! "
        "And when school boards try to fix this, private consultants charge up to $25,000 just to do an initial study. "
        "Most schools give up before they even start.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 3: The Secret: Federal Direct Pay Cash
    # ---------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header_bar(s3, 3, 10)
    add_slide_header(s3, "The Opportunity", "The Clean Energy Law School Boards Don't Know About",
                     "Under the new Inflation Reduction Act, the federal government writes cash checks directly to schools.")

    card_w3 = Inches(3.8)
    card_h3 = Inches(4.0)
    card_y3 = Inches(1.9)

    cards_s3 = [
        ("30% Base", "GUARANTEED CASH BACK", COLOR_GREEN, [
            "Federal IRS cash check covering 30% of cost",
            "Direct payment to the school district treasury",
            "No tax liability needed—public schools qualify directly!"
        ]),
        ("+10% to +20%", "BONUS FEDERAL CASH", COLOR_SOLAR, [
            "+10% extra bonus for American-made steel & panels",
            "+10% extra bonus for Title I low-income schools",
            "Puts the biggest grants into communities that need it most"
        ]),
        ("Up to 50%", "TOTAL FEDERAL GRANT", COLOR_GREEN, [
            "Up to half the solar canopy is paid by the government",
            "Districts pay only the remaining net balance",
            "Yet over 90% of school boards have never heard of it!"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(cards_s3):
        x = Inches(0.6 + idx * 4.15)
        add_card(s3, x, card_y3, card_w3, card_h3, top_accent_color=col)
        tb = s3.shapes.add_textbox(x + Inches(0.2), card_y3 + Inches(0.18), card_w3 - Inches(0.4), card_h3 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(38)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom Explanation
    add_card(s3, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_GREEN)
    tb_bot3 = s3.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b3 = tb_bot3.text_frame
    tf_b3.word_wrap = True
    p = tf_b3.paragraphs[0]
    p.text = "HOW 'DIRECT PAY' (SECTION 6417) WORKS"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p2 = tf_b3.add_paragraph()
    p2.text = "Because public schools don't pay taxes, the government used to shut them out of solar tax credits. Now, the IRS sends an actual cash reimbursement check straight to the district."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s3,
        "[0:50 - 1:15] 'Here is the exciting part that almost nobody knows. "
        "In 2022, a new federal law called 'Direct Pay' was passed. "
        "Historically, public schools couldn't get solar tax credits because schools don't pay taxes. "
        "Now, under Section 6417, the IRS will literally write an actual CASH check directly to public school districts! "
        "They pay a 30% base grant, plus an extra 10% for American steel and 10% for Title I schools. "
        "That means the federal government can cover up to 50% of the entire solar canopy! "
        "The problem? Over 90% of school boards have no idea this money exists.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 4: What We Built: SolarSchools USA
    # ---------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header_bar(s4, 4, 10)
    add_slide_header(s4, "The Solution", "Solar Feasibility in Seconds, Not Months",
                     "A web platform empowering students and school boards to test their campus with real data.")

    card_w4 = Inches(3.8)
    card_h4 = Inches(4.0)
    card_y4 = Inches(1.9)

    steps = [
        ("Step 1", "PICK ANY CAMPUS", COLOR_SOLAR, [
            "Interactive satellite map of 18 Bay Area schools",
            "Pins directly to the physical parking lot",
            "Covers High Schools, Middle Schools & Elementary"
        ]),
        ("Step 2", "SIMULATE SOLAR", COLOR_GREEN, [
            "Runs Department of Energy (NREL) solar physics",
            "Calculates kilowatt capacity and monthly power",
            "Applies real local commercial electricity rates"
        ]),
        ("Step 3", "GET BOARD BRIEF", COLOR_STANFORD, [
            "Generates a 1-page financial action brief",
            "Calculates the exact federal cash grant",
            "Includes a draft resolution ready for board votes"
        ])
    ]
    for idx, (step_tag, step_title, col, bullets) in enumerate(steps):
        x = Inches(0.6 + idx * 4.15)
        add_card(s4, x, card_y4, card_w4, card_h4, top_accent_color=col)
        tb = s4.shapes.add_textbox(x + Inches(0.2), card_y4 + Inches(0.18), card_w4 - Inches(0.4), card_h4 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = step_tag.upper()
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = step_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom Live Demo Banner
    add_card(s4, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_SOLAR)
    tb_bot4 = s4.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b4 = tb_bot4.text_frame
    tf_b4.word_wrap = True
    p = tf_b4.paragraphs[0]
    p.text = "BUILT FOR STUDENTS AND COMMUNITY ADVOCATES"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p2 = tf_b4.add_paragraph()
    p2.text = "No expensive consultants. No engineering degrees needed. Any student can walk into a school board meeting with the numbers in hand."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s4,
        "[1:15 - 1:40] 'So I decided to build a solution: SolarSchools USA. "
        "It is a web application designed so any high school student or parent can use it. "
        "Step 1: you select your school from our database of 18 Bay Area campuses. It zooms right onto the parking lot. "
        "Step 2: in real time, it connects to the Department of Energy's solar engine and calculates how many panels fit, "
        "how much electricity they generate, and how much money the school saves. "
        "Step 3: with one click, you download a complete School Board Action Brief with the exact financial breakdown "
        "and a template resolution ready to present to school board trustees.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 5: The Math Made Simple
    # ---------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header_bar(s5, 5, 10)
    add_slide_header(s5, "Behind The Scenes", "Real Science, Zero Guesswork",
                     "How we calculate solar potential accurately without needing an on-site engineer.")

    card_w5 = Inches(3.8)
    card_h5 = Inches(4.0)
    card_y5 = Inches(1.9)

    specs = [
        ("65% Lot Cover", "PRACTICAL PARKING DESIGN", COLOR_SOLAR, [
            "Leaves 24-foot driving aisles open for traffic",
            "Keeps 14-foot vertical clearance for school buses",
            "Preserves ADA accessible pathways and fire lanes"
        ]),
        ("200 W / m²", "COMMERCIAL SOLAR PANELS", COLOR_SOLAR, [
            "Models high-efficiency commercial solar canopies",
            "Accounts for summer heat and dust loss",
            "Calibrated against active school arrays in Cupertino"
        ]),
        ("NREL Engine", "U.S. DEPT OF ENERGY DATA", COLOR_GREEN, [
            "Queries live satellite solar data for exact GPS coords",
            "Models local weather, sun angles, and seasons",
            "Includes instant smart backup so it never crashes"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(specs):
        x = Inches(0.6 + idx * 4.15)
        add_card(s5, x, card_y5, card_w5, card_h5, top_accent_color=col)
        tb = s5.shapes.add_textbox(x + Inches(0.2), card_y2 + Inches(0.18), card_w5 - Inches(0.4), card_h5 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom Calibrated Note
    add_card(s5, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_SOLAR)
    tb_bot5 = s5.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b5 = tb_bot5.text_frame
    tf_b5.word_wrap = True
    p = tf_b5.paragraphs[0]
    p.text = "ENGINEERED FOR ACCURACY"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p2 = tf_b5.add_paragraph()
    p2.text = "We don't guess: our calculations are calibrated directly against active solar canopies in Cupertino Union and Fremont Union High School District."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s5,
        "[1:40 - 2:05] 'We made sure the numbers are rock-solid. "
        "We don't assume the entire parking lot is covered in solar. We use an empirical 65% coverage factor, "
        "which reserves 24-foot driving aisles, ADA handicap spots, and a full 14-foot vertical clearance for yellow school buses. "
        "Then, we connect directly to the Department of Energy's NREL database to pull exact satellite sunshine numbers "
        "for the school's precise coordinates, accounting for summer heat, dust, and winter sun angles. "
        "It's the same math that professional engineering firms use, but packaged so anyone can run it in seconds.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 6: Real Proof: Monta Vista vs. Palo Alto High
    # ---------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header_bar(s6, 6, 10)
    add_slide_header(s6, "Case Study", "The Tale of Two Schools: Leaders vs. Lost Cash",
                     "See what happens when a school takes action versus letting asphalt sit idle.")

    card_w6 = Inches(5.9)
    card_h6 = Inches(5.0)

    # Left: Monta Vista
    add_card(s6, Inches(0.6), Inches(1.9), card_w6, card_h6, top_accent_color=COLOR_GREEN)
    tb_mv = s6.shapes.add_textbox(Inches(0.85), Inches(2.05), card_w6 - Inches(0.5), card_h6 - Inches(0.3))
    tf_mv = tb_mv.text_frame
    tf_mv.word_wrap = True
    p = tf_mv.paragraphs[0]
    p.text = "MONTA VISTA HIGH (CUPERTINO)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    p = tf_mv.add_paragraph()
    p.text = "ACTIVE SOLAR LEADER"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(1)

    p = tf_mv.add_paragraph()
    p.text = "$145,000 / yr"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_before = Pt(4)

    mv_bullets = [
        "Completed 550 kW solar carports across student lot",
        "Shades cars, provides EV chargers, and cuts campus heat",
        "Our model predicted $145K savings; actual FUHSD bill records show $139K!",
        "Empirical accuracy within 4.17% of actual utility bills"
    ]
    for b in mv_bullets:
        p_b = tf_mv.add_paragraph()
        p_b.text = f"- {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = COLOR_WHITE if "4.17%" in b else COLOR_MUTED
        p_b.font.bold = True if "4.17%" in b else False
        p_b.space_before = Pt(5)

    # Right: Palo Alto High
    add_card(s6, Inches(6.8), Inches(1.9), card_w6, card_h6, top_accent_color=COLOR_RED)
    tb_pa = s6.shapes.add_textbox(Inches(7.05), Inches(2.05), card_w6 - Inches(0.5), card_h6 - Inches(0.3))
    tf_pa = tb_pa.text_frame
    tf_pa.word_wrap = True
    p = tf_pa.paragraphs[0]
    p.text = "PALO ALTO HIGH (PALO ALTO)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    p = tf_pa.add_paragraph()
    p.text = "UNSHADED OPPORTUNITY"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUBTLE
    p.space_before = Pt(1)

    p = tf_pa.add_paragraph()
    p.text = "-$140,000 / yr"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_before = Pt(4)

    pa_bullets = [
        "7,200 m² of empty asphalt sits 100% unshaded",
        "District surrenders $140,000 every year to utility bills",
        "Leaves an unclaimed $754,000 federal cash grant on the table",
        "Cost of waiting 5 years: Over $700,000 lost from classrooms!"
    ]
    for b in pa_bullets:
        p_b = tf_pa.add_paragraph()
        p_b.text = f"- {b}"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = COLOR_WHITE if "Cost of waiting" in b else COLOR_MUTED
        p_b.font.bold = True if "Cost of waiting" in b else False
        p_b.space_before = Pt(5)

    p_call = tf_pa.add_paragraph()
    p_call.text = "That $140,000 lost each year is enough to pay for 2 full-time teachers!"
    p_call.font.size = Pt(10.5)
    p_call.font.bold = True
    p_call.font.color.rgb = COLOR_AMBER
    p_call.space_before = Pt(10)

    set_speaker_notes(s6,
        "[2:05 - 2:35] 'Let's look at real-world proof right here in Silicon Valley. "
        "At Monta Vista High in Cupertino, they installed 550 kW of solar carports in 2021. "
        "Our software modeled that they would save $145,000 a year. When we checked the district's actual published utility bills, "
        "they saved $139,200. That's a 4% match with real life! "
        "Now look just 10 miles away at Palo Alto High. They have a massive parking lot baking in the sun, "
        "paying $140,000 a year to the power company that they don't need to pay. "
        "And there is a $754,000 cash grant from the federal government waiting for them. "
        "That $140,000 every year could pay for two full-time teachers or hundreds of laptops!'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 7: The Money: Fast Payback, Millions in Savings
    # ---------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header_bar(s7, 7, 10)
    add_slide_header(s7, "The Return on Investment", "Fast Payback, 25 Years of Free Electricity",
                     "Solar canopies pay for themselves faster than almost any school facility project.")

    card_w7 = Inches(2.8)
    card_h7 = Inches(4.0)
    card_y7 = Inches(1.9)

    stats7 = [
        ("3.7 Years", "RAPID PAYBACK", COLOR_GREEN, [
            "Pays for itself in under 4 years",
            "Drops from 6+ years thanks to Direct Pay",
            "Faster than almost any school bond project"
        ]),
        ("$750K+", "FEDERAL CASH CHECK", COLOR_SOLAR, [
            "Direct cash reimbursement from IRS",
            "Covers 30% to 50% of the total canopy cost",
            "Paid directly to the district treasury"
        ]),
        ("$140K/yr", "ANNUAL BILL SAVINGS", COLOR_GREEN, [
            "Clean solar power offsets expensive peak grid rates",
            "Protects district from rising utility prices",
            "Savings start the first month it's turned on"
        ]),
        ("$9.8M", "25-YEAR DIVIDEND", COLOR_AMBER, [
            "Total cumulative net savings over 25 years",
            "Accounts for panel aging and maintenance costs",
            "Permanent long-term funding for school programs"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(stats7):
        x = Inches(0.6 + idx * 3.1)
        add_card(s7, x, card_y7, card_w7, card_h7, top_accent_color=col)
        tb = s7.shapes.add_textbox(x + Inches(0.15), card_y7 + Inches(0.18), card_w7 - Inches(0.3), card_h7 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(30)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom Takeaway Card
    add_card(s7, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_GREEN)
    tb_bot7 = s7.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b7 = tb_bot7.text_frame
    tf_b7.word_wrap = True
    p = tf_b7.paragraphs[0]
    p.text = "WHAT DOES A $9.8M DIVIDEND MEAN FOR A SCHOOL?"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p2 = tf_b7.add_paragraph()
    p2.text = "It means permanent funding for STEM labs, art and music teachers, student mental health counselors, and zero school bond tax hikes."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s7,
        "[2:35 - 3:00] 'When you look at the financials, it's an absolute no-brainer. "
        "Normally, a solar canopy might take 6 to 7 years to pay back. "
        "With the federal Direct Pay check covering up to 40% or 50% upfront, the payback period drops to just 3.7 years! "
        "After year four, all that electricity is pure profit for the school district. "
        "Over the 25-year lifespan of the panels, even after paying for washing and maintenance, "
        "a single high school generates nearly 10 million dollars in net savings. "
        "That's permanent money for science labs, clubs, and teachers without raising local property taxes.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 8: Real Campus Upgrades
    # ---------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header_bar(s8, 8, 10)
    add_slide_header(s8, "Campus Impact", "More Than Just Power: Real Upgrades for Students",
                     "Solar canopies turn an ugly, boiling parking lot into high-tech school infrastructure.")

    card_w8 = Inches(3.8)
    card_h8 = Inches(4.0)
    card_y8 = Inches(1.9)

    benefits = [
        ("40°F Cooler", "SHADE & HEAT RELIEF", COLOR_SOLAR, [
            "Cuts vehicle interior temperatures by up to 40°F",
            "Keeps cars cool for teachers and high school drivers",
            "Shades elementary and middle school play blacktops",
            "Combats urban heat waves during California autumns"
        ]),
        ("Clean EVs", "POWERING OUR TEACHERS", COLOR_GREEN, [
            "Built-in Level 2 EV charging stations under the canopies",
            "Powers teachers' daily commute with 100% clean sunshine",
            "Ready to charge future electric yellow school buses",
            "Reduces local car exhaust around campus drop-off zones"
        ]),
        ("Resilient", "CAMPUS EMERGENCY POWER", COLOR_AMBER, [
            "Microgrid-ready for future battery storage",
            "Can keep lights, Wi-Fi, and refrigeration on during outages",
            "Turns public schools into neighborhood emergency hubs",
            "Provides student science dashboards with live solar data"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(benefits):
        x = Inches(0.6 + idx * 4.15)
        add_card(s8, x, card_y8, card_w8, card_h8, top_accent_color=col)
        tb = s8.shapes.add_textbox(x + Inches(0.2), card_y8 + Inches(0.18), card_w8 - Inches(0.4), card_h8 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom Safety Note
    add_card(s8, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_SOLAR)
    tb_bot8 = s8.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b8 = tb_bot8.text_frame
    tf_b8.word_wrap = True
    p = tf_b8.paragraphs[0]
    p.text = "BUILT WITH STUDENT SAFETY IN MIND"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p2 = tf_b8.add_paragraph()
    p2.text = "Commercial steel canopies provide covered walkways during winter rainstorms, night lighting for safer athletic events, and clean EV plugs."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s8,
        "[3:00 - 3:20] 'Beyond the money, this transforms what our campuses feel like every day. "
        "Parking lots go from boiling asphalt into shaded community assets. Cars stay 40 degrees cooler, "
        "and teachers get free Level 2 EV charging powered directly by the sun. "
        "Elementary school kids get shaded play areas so blacktop doesn't burn their knees. "
        "And in emergencies or wildfire blackouts, these systems can keep emergency shelters and food refrigeration powered. "
        "It turns our schools into true clean energy hubs.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 9: Growing Beyond the Bay Area
    # ---------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header_bar(s9, 9, 10)
    add_slide_header(s9, "The Vision", "Phase 1 is Live. Here's Where We Go Next.",
                     "How one student project scales to 100,000 public schools across the United States.")

    card_w9 = Inches(3.8)
    card_h9 = Inches(4.0)
    card_y9 = Inches(1.9)

    phases = [
        ("Phase 1", "BAY AREA PILOT (LIVE)", COLOR_SOLAR, [
            "18 local campuses mapped & verified today",
            "Covers Cupertino, Palo Alto, San Jose & Sunnyvale",
            "High Schools, Middle Schools, and Elementary",
            "100% verified against real utility rates"
        ]),
        ("Phase 2", "CALIFORNIA STATEWIDE", COLOR_GREEN, [
            "Expanding to 10,000 public schools across CA",
            "Focusing on hot Central Valley school districts",
            "Targeting Title I low-income schools for max federal cash",
            "Supports California's clean energy school mandates"
        ]),
        ("Phase 3", "NATIONWIDE EXPANSION", COLOR_AMBER, [
            "Scaling to 100,000 public campuses across 50 states",
            "Targeting Midwest & Sunbelt coal-heavy power grids",
            "Replacing dirty coal power gives 2.5x more carbon cut per watt!",
            "Empowers youth climate clubs in every state"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(phases):
        x = Inches(0.6 + idx * 4.15)
        add_card(s9, x, card_y9, card_w9, card_h9, top_accent_color=col)
        tb = s9.shapes.add_textbox(x + Inches(0.2), card_y9 + Inches(0.18), card_w9 - Inches(0.4), card_h9 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Bottom National Scale Note
    add_card(s9, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_GREEN)
    tb_bot9 = s9.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b9 = tb_bot9.text_frame
    tf_b9.word_wrap = True
    p = tf_b9.paragraphs[0]
    p.text = "THE NATIONAL IMPACT"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p2 = tf_b9.add_paragraph()
    p2.text = "If just 10% of America's schools install solar parking canopies, we save school districts over $800M every single year and eliminate millions of tons of emissions."
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s9,
        "[3:20 - 3:35] 'Here is where we are heading. Phase 1 is done and live today: 18 schools right here in our backyard. "
        "Phase 2 scales across California to 10,000 schools, prioritizing hot Central Valley districts and Title I schools. "
        "And Phase 3 scales nationwide to 100,000 schools across all 50 states. "
        "In places like the Midwest, power grids still rely on dirty coal, so a solar panel installed on an Ohio school "
        "cuts two and a half times more carbon than the same panel in California! "
        "If just 10% of US schools build solar canopies, we save education budgets 800 million dollars every single year.'"
    )

    # ---------------------------------------------------------------------
    # SLIDE 10: Call to Action: The Student Voice
    # ---------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header_bar(s10, 10, 10)
    add_slide_header(s10, "Take Action", "Putting the Power in Students' Hands",
                     "How any high school student can walk into their school board meeting and kickstart clean energy.")

    card_w10 = Inches(3.8)
    card_h10 = Inches(4.0)
    card_y10 = Inches(1.9)

    actions = [
        ("Step 1", "FIND YOUR SCHOOL", COLOR_SOLAR, [
            "Open SolarSchools USA on any laptop or phone",
            "Type your school's name to view your parking lot",
            "See your school's exact energy and savings in 5 seconds"
        ]),
        ("Step 2", "PRINT THE BRIEF", COLOR_GREEN, [
            "Download our automated 1-page Action Brief",
            "Shows the exact federal cash grant for your district",
            "Share it with your principal, teachers, and student council"
        ]),
        ("Step 3", "SPEAK TO TRUSTEES", COLOR_STANFORD, [
            "Use our ready-to-vote School Board Resolution",
            "Show trustees how to claim federal cash before it expires",
            "Turn student climate advocacy into real, funded infrastructure"
        ])
    ]
    for idx, (stat, label, col, bullets) in enumerate(actions):
        x = Inches(0.6 + idx * 4.15)
        add_card(s10, x, card_y10, card_w10, card_h10, top_accent_color=col)
        tb = s10.shapes.add_textbox(x + Inches(0.2), card_y10 + Inches(0.18), card_w10 - Inches(0.4), card_h10 - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(2)
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"- {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_MUTED
            p_b.space_before = Pt(6)

    # Final Hero Callout Card
    add_card(s10, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.85), border_color=COLOR_STANFORD)
    tb_bot10 = s10.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    tf_b10 = tb_bot10.text_frame
    tf_b10.word_wrap = True
    p = tf_b10.paragraphs[0]
    p.text = "THE TIME TO ACT IS NOW"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR
    p2 = tf_b10.add_paragraph()
    p2.text = "Our schools have the sunshine. The federal government has the cash. Let's shade our parking lots and power our classrooms!"
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(2)

    set_speaker_notes(s10,
        "[3:35 - 3:50] 'To wrap up: students shouldn't have to wait 10 years for school boards to hire expensive consultants. "
        "With SolarSchools USA, any student can look up their campus in five seconds, print out a professional brief, "
        "and walk up to the microphone at their school board meeting this Tuesday. "
        "Our schools have the sunshine. The federal government has the cash. Let's shade our parking lots and power our classrooms. "
        "Thank you so much, and I welcome any questions!'"
    )

    output_path = "/home/balaji/personal/pranav/svyca2026/SolarSchoolsUSA_PitchDeck.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint deck: {output_path}")

    # Copy to user home directory as well for easy access
    home_path = os.path.expanduser("~/SolarSchoolsUSA_PitchDeck.pptx")
    try:
        import shutil
        shutil.copyfile(output_path, home_path)
        print(f"Copied to home folder: {home_path}")
    except Exception as e:
        print(f"Could not copy to home: {e}")

if __name__ == "__main__":
    build_deck()
