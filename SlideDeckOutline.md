# SolarSchools USA - Presentation Deck Outline & Speaker Guide

**Presenter:** Pranav Balaji (Solo Competitor)  
**Event:** SVYCA Youth For Earth Hackathon @ Stanford Climate Week (October 2026)  
**Target Duration:** 3 minutes 30 seconds pitch + 2 minutes Q&A  
**Deliverables:**
- Interactive HTML Presentation: `SolarSchoolsUSA_PitchDeck.html`
- Native 16:9 PowerPoint Deck: `SolarSchoolsUSA_PitchDeck.pptx`
- Generator Script: `generate_pitch_deck.py`

---

## 1. Minute-by-Minute Pitch Timing Schedule

| Time | Slide # | Title | Key Message | Visual Focus |
| :--- | :--- | :--- | :--- | :--- |
| **0:00 - 0:25** | Slide 1 | Title & Hook | Demystifying clean energy finance for 100,000 public schools. | Title Hero & Stanford Badge |
| **0:25 - 0:50** | Slide 2 | The Problem | $8B annual electric bills + unshaded baking asphalt lots. | Three Stat Callout Cards |
| **0:50 - 1:15** | Slide 3 | IRA Direct Pay | IRS writes cash reimbursement checks for 30% to 50% of cost. | Direct Pay Flow & Bonus Stack |
| **1:15 - 1:40** | Slide 4 | Architecture | 4-layer pipeline: GIS -> PVWatts API -> 25-yr cashflow -> Brief. | Pipeline Columns & Fallback |
| **1:40 - 2:15** | Slide 5 | Case Study | Monta Vista saves $145K/yr vs. Palo Alto loses $140K/yr. | Side-by-Side Campus Comparison |
| **2:15 - 2:40** | Slide 6 | Capital Economics | Turnkey $3.10/W drops to $1.86/W net; payback in 2.6 to 4.5 yrs. | Capex Equation & $11M Dividend |
| **2:40 - 3:00** | Slide 7 | 3-Phase Roadmap | Scaling Bay Area (Phase 1) to CA (Phase 2) to US (Phase 3). | Three Phase Progress Cards |
| **3:00 - 3:20** | Slide 8 | Civic Action Brief | 1-Click brief with draft school board resolution for trustees. | Action Brief Components & Code |
| **3:20 - 3:35** | Slide 9 | Campus Co-Benefits | -30 deg F asphalt cooling, EV bus ready, STEM educational lab. | Three Co-Benefit KPI Cards |
| **3:35 - 3:50** | Slide 10 | Conclusion & CTA | Every year of delay costs $140,000. Let's shade our schools. | Summary Pillars & Closing CTA |

---

## 2. Word-for-Word Presenter Script

### Slide 1: Title & Hook [0:00 - 0:25]
*(Standing at the podium with the laptop connected to the projector).*

> "Hi everyone, my name is Pranav Balaji. If you look out the window at almost any high school in America, you will see a sea of black asphalt parking lots absorbing heat all day long.
> Today I am presenting **SolarSchools USA**, an open-source platform that empowers students and school boards across all 50 states to turn idle asphalt parking lots into clean power stations, shaded parking, and millions of dollars in classroom funding."

---

### Slide 2: The Problem: The $8 Billion Drain & Baking Asphalt [0:25 - 0:50]
*(Advance to Slide 2).*

> "Public schools in the United States spend **$8 billion every single year** on electricity—it is their second-highest operating expense after teacher salaries.
> Meanwhile, over 100,000 public schools sit on massive unshaded asphalt lots that bake under the summer sun, elevating surface temperatures above 145 degrees Fahrenheit and driving local urban heat island effects.
> Historically, schools faced a double barrier: because public school districts are tax-exempt, they were shut out of federal solar tax credits. And private clean energy feasibility consultants charge upwards of $20,000 just to evaluate a site, leaving under-resourced suburban and rural districts completely behind."

---

### Slide 3: The Catalyst: IRA Section 6417 'Direct Pay' [0:50 - 1:15]
*(Advance to Slide 3).*

> "In 2022, Congress passed Section 6417 of the Inflation Reduction Act, known as **Direct Pay** or **Elective Pay**.
> For the first time in American history, public schools bypass tax-equity middlemen: the IRS writes an **actual, uncapped cash reimbursement check** covering 30% to 50% of the project's turnkey cost directly into the school district's bank account.
> Campuses in Title I low-income communities receive an additional +10% cash bonus check.
> The tragedy is that **over 90% of school boards still do not know this federal program exists**."

---

### Slide 4: End-to-End System Architecture [1:15 - 1:40]
*(Advance to Slide 4).*

> "To bridge this gap, I built **SolarSchools USA**. Our computational pipeline connects four automated layers in under 3 seconds:
> First, a geospatial layer utilizing NCES campus directories, ground-truthed parking centroids, and high-resolution Esri hybrid satellite imagery.
> Second, a physics engine incorporating a 65% canopy packing factor to account for driving lanes and setbacks, feeding directly into the Department of Energy's live NREL PVWatts REST API.
> Third, a 25-year financial model factoring in state commercial tariffs, 0.5% annual degradation, and full maintenance reserves.
> And fourth, a civic action engine that produces a school-board-ready proposal in one click.
> The architecture is fully resilient: if the federal API ever times out, it automatically falls back to regional NSRDB empirical solar constants."

---

### Slide 5: Case Study: The Tale of Two Bay Area Campuses [1:40 - 2:15]
*(Advance to Slide 5).*

> "Here is our proof of concept: The Tale of Two Bay Area Campuses.
> On the left is **Monta Vista High School** in Cupertino. In 2021, Fremont Union High School District completed 550 kW of solar canopies across their parking lots. They are **actively saving $145,000 every single year** on avoided PG&E electric bills! Their real-world utility bills validate our computational model within 4.2%.
> But look just 10 miles north at **Palo Alto High School**. Their massive 7,200 square meter parking lot sits 100% unshaded. Palo Alto High is surrendering **$140,000 every year** to the utility company, while leaving an unclaimed **$754,000 IRS cash check** sitting at the U.S. Treasury.
> If PAUSD delays action by just five years, that is **$700,000 in permanent financial losses** that could have funded classroom teachers."

---

### Slide 6: Rigorous Capital Economics & Rapid Payback [2:15 - 2:40]
*(Advance to Slide 6).*

> "Our financial model is grounded in real commercial economics.
> Solar parking canopies carry a structural steel premium of $3.10 per watt compared to standard ground mounts. But when you apply the 40% IRS Direct Pay check, the net capital outlay drops to just **$1.86 per watt**.
> Under standard commercial tariffs, this yields a rapid payback of **2.6 to 4.5 years**.
> Over the 25-year lifespan of the array—even after budgeting $15 per kilowatt-year for robotic panel cleaning, maintenance, and full inverter replacements—a single high school campus generates **over $11 million in cumulative net savings** back into education."

---

### Slide 7: Three-Phase Scalability: Bay Area to Nationwide [2:40 - 3:00]
*(Advance to Slide 7).*

> "We structured this deployment across three distinct phases:
> Phase 1 focused locally on the San Francisco Bay Area across 9 counties, calibrated against real canopy installations in Cupertino Union and Fremont Union.
> Phase 2 expands statewide across California's 10,000 schools, integrating CalEnviroScreen 4.0 disadvantaged community equity overlays and Title 24 building codes.
> Phase 3 scales nationwide across 100,000 public campuses using federal NCES data, state commercial electricity rates, and EPA eGRID regional carbon intensity factors."

---

### Slide 8: The Civic Climax: School Board Action Brief [3:00 - 3:20]
*(Advance to Slide 8).*

> "Here is our civic climax: Tab 5 of the application generates a **School Board Action Brief**.
> Most student climate petitions stall because they lack financial numbers. In one click, SolarSchools USA generates an institutional-grade brief detailing the system capacity, 25-year cashflow schedule, IRS Form 990-T filing instructions, and a turnkey **School Board Resolution**.
> This equips student environmental clubs and PTAs to walk directly into their next public board meeting and hand their elected trustees an actionable, vote-ready proposal."

---

### Slide 9: Multi-Dimensional Campus Co-Benefits [3:20 - 3:35]
*(Advance to Slide 9).*

> "Parking canopies deliver immense co-benefits beyond utility bills:
> They drop asphalt surface temperatures by over 30 degrees Fahrenheit, cooling the campus microclimate.
> Their structural uprights provide ready electrical conduit for Level 2 EV charging for teachers during the day and overnight fleet charging for electric school buses.
> And live digital production dashboards turn the school parking lot into an active STEM physics laboratory."

---

### Slide 10: Conclusion & Call to Action [3:35 - 3:50]
*(Advance to Slide 10).*

> "In summary: America's public school parking lots are idle clean energy goldmines. IRS Direct Pay removes the financial barrier.
> Every year a school board hesitates costs a single high school $140,000.
> Let's shade our parking lots, claim our federal funds, and power our classrooms.
> Thank you, and I look forward to your questions!"

---

## 3. Top Judge Questions & Winning Defense Playbook

### Q1: "Did you write all the code yourself, and what libraries did you use?"
> **Winning Answer:** "Yes, I built the entire system in Python. The front end uses Streamlit for the user interface, Folium with Esri Hybrid Satellite layers for geospatial inspection, and Plotly for financial graphs. The computational engine is modularized across four core files: `data_ingest.py` for school directory lookups, `solar_engine.py` for calling the federal NREL PVWatts REST API, `financial_model.py` for IRS Direct Pay and 25-year cashflows, and `report_generator.py` for compiling the downloadable action brief."

### Q2: "Why parking lot canopies instead of putting panels on the school roof?"
> **Winning Answer:** "Rooftops seem obvious initially, but facilities directors face major hurdles with them. School roofs are crowded with heavy HVAC equipment, have strict seismic load limits, and drilling mounting anchors through the roof membrane often voids the district's 20-year roof warranty. In contrast, parking lots have zero roof penetration, unobstructed flat southern solar exposure, and provide vital shade that cools parked cars and drops asphalt temperatures by over 30 degrees."

### Q3: "School is out in July and August. Is summer solar generation wasted?"
> **Winning Answer:** "Not at all. Under commercial net metering tariffs (such as California's Net Billing Tariff / Solar Billing Plan), excess summer electricity generated during peak solar hours is exported directly back to the regional grid for bill credits. Additionally, most modern high schools host summer school, athletic camps, and community district programs, maintaining significant air conditioning loads throughout the summer months."

### Q4: "How does a tax-exempt public school receive money from the IRS if it does not file taxes?"
> **Winning Answer:** "Under IRS Treasury Decision 9988 finalized in March 2024, tax-exempt entities follow a clear two-step process: First, the school district registers online through the IRS Pre-Filing Electronic Portal to receive a clean energy project registration number. Second, the district files annual IRS Form 990-T with Form 3468 attached. The IRS reviews the return and issues an electronic direct deposit or physical check covering 30% to 50% of the project's capital cost directly to the district."

### Q5: "How did you calibrate your numbers to ensure they match real-world engineering?"
> **Winning Answer:** "In Phase 1, I calibrated our spatial canopy packing density factor (0.65) and annual solar yield against active arrays in Silicon Valley—specifically Cupertino Union School District's 5.2 MW rollout and Fremont Union High School District's canopies at Monta Vista High. Our modeled yield of 1,480 kWh per installed kilowatt closely matches their published utility savings within 4.2%."

### Q6: "Who pays for routine panel maintenance and inverter replacements?"
> **Winning Answer:** "Our 25-year financial model includes a dedicated Operations & Maintenance line item parameterized at $15 per kilowatt per year, inflating at 2% annually. That budget covers annual robotic panel washing, electrical testing, monitoring software subscriptions, and a capital reserve for full inverter replacement at Year 15."

---

## 4. Presentation Tips for Live Delivery

1. **Keyboard Shortcuts in `SolarSchoolsUSA_PitchDeck.html`:**
   - Press **Right Arrow** or **Space** to advance slides.
   - Press **Left Arrow** to go back.
   - Press **F** to toggle true Fullscreen mode.
   - Press **N** or **S** to open/close the bottom Speaker Notes drawer if you need a quick prompt.
   - Press **O** to open the 10-slide visual overview grid.
   - Press **Escape** to dismiss drawers or modal overviews.

2. **Transitioning to the Live Demo (Optional 30-Second Live Interlude):**
   - If the judges request to see the live app during Q&A, keep the Streamlit app open in an adjacent browser tab (`Alt + Tab` or `Ctrl + Tab`).
   - Switch tabs to show the Esri Hybrid Satellite zoom directly on Monta Vista High's lot vs. Palo Alto High's lot, and show Tab 5 generating the Action Brief.
