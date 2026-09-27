# Student Pitch & Judge Defense Guide: SolarSchools USA
**Prepared for Pranav Balaji (Solo High School Competitor)**  
*SVYCA Youth For Earth Hackathon @ Stanford Climate Week (October 25, 2026)*

---

## 1. The 30-Second Elevator Pitch
> *"Public schools in America spend $8 billion every single year on electricity—it's their highest expense after teacher salaries. Meanwhile, schools have massive asphalt parking lots that bake in the hot sun. In the past, schools couldn't afford solar consultants, and because schools don't pay taxes, they couldn't use federal solar tax credits.*  
> *Under the 2022 Inflation Reduction Act, the rules changed: the IRS now writes a **direct cash reimbursement check for 30% to 50% of the cost** to public school districts.*  
> *I built **SolarSchools USA**, a free geospatial web app that lets any student or school board in all 50 states click on their high school, calculate their solar canopy size using Department of Energy physics, and see the exact dollar amount of the IRS cash check and power bill savings in under 3 seconds."*

---

## 2. The 3-Minute Live Hackathon Pitch Script (Word-for-Word)

### [0:00 - 0:45] The Hook & The Problem
*(Standing at the podium with the laptop plugged into the projector. Show the title screen).*
> *"Hi everyone, my name is Pranav Balaji. If you look out the window at almost any high school in America, you'll see a sea of black asphalt parking lots absorbing heat all day long.  
> Energy is the second-largest cost for public school districts, costing taxpayers over **$8 billion a year**.  
> Here in Silicon Valley, wealthy districts like Cupertino and Fremont Union have already built solar carports. But for thousands of suburban and rural schools across California and the country, they don't have $10,000 to hire private solar consultants, so they leave millions of dollars on the table.  
> In 2022, Congress passed Section 6417 of the Inflation Reduction Act—called 'Direct Pay.' For the first time in history, the IRS writes an **actual cash reimbursement check** covering 30% to 50% of clean energy projects for tax-exempt public schools. But over 90% of school boards still don't know this exists."*

### [0:45 - 2:15] The Live Tool Demonstration: The Tale of Two Districts
*(Click on the screen and interact with the Streamlit app).*
> *"To solve this, I built **SolarSchools USA**. Our app highlights a stark contrast: **districts that took action and are saving millions, versus districts leaving money on the table.**  
>  
> *(Step 1 - Show a Leader Campus)*: *Let's first look at an implemented leader—**Monta Vista High School** in Cupertino. They partnered with ENGIE to build 550 kW of solar canopies over their student and staff lots. You can see the green status banner: they are **actively saving $145,000 every single year** on their electric bills. Their real-world utility bills prove our physics and financial model works!*  
>  
> *(Step 2 - Show an Unshaded Campus Losing Money)*: *Now, look just 10 miles away at **Palo Alto High School**. Their massive 7,200 m² parking lot is 100% unshaded asphalt. You can see the red alert banner: **this campus is surrendering $140,000 every year directly to the utility company in avoidable power bills!** If the school board delays action by just 5 years, that's a **$700,000 penalty of inaction**—and an unclaimed **$750,000 IRS cash check** left behind at the U.S. Treasury.*  
>  
> *(Step 3 - Nationwide Scale)*: *And this isn't just a California story. Let's switch to Phase 3 and look at **Westlake High School in Austin, Texas**. Under the Texas sun, their unshaded lot is losing $145,000/year to utility bills while leaving an astonishing **$1.52 million IRS Direct Pay check** unclaimed!"*

### [2:15 - 2:45] Phased Roadmap & The Civic Climax
*(Click on Tab 5: School Board Action Brief).*
> *"We built this project in three distinct phases:  
> - **Phase 1: Bay Area**—ground-truthed against real solar carports at Monta Vista, Cupertino High, and CUSD's 25 elementary and middle schools.  
> - **Phase 2: California Statewide**—incorporating CalEnviroScreen equity overlays and Title 24 building codes.  
> - **Phase 3: Nationwide USA**—scaling across all 50 states using federal NCES data and state utility rates.  
> But the most important feature is right here: **Tab 5**. Any student environmental club or PTA can click **'Download School Board Action Brief'**. In one second, it generates a complete, professional proposal calculating the cost of delay, exact engineering specs, IRS citations, and sample school board resolution text that students can take to their next school board meeting."*

### [2:45 - 3:00] Closing Statement
> *"SolarSchools USA democratizes climate finance, turning idle asphalt into clean power and classroom money. Thank you, and I'd love to answer any questions!"*

---

## 3. Core Concepts Explained Simply (Like You're Talking to a Friend)

If a judge asks you to explain any concept, use these simple mental models:

| Technical Term | What It Means | Simple Everyday Analogy |
| :--- | :--- | :--- |
| **kW (Kilowatt)** | Power capacity (how big the solar array is right now). | Like the **horsepower** of a car engine. |
| **kWh (Kilowatt-Hour)** | Total energy generated over time (e.g., in a month or year). | Like the **odometer (miles driven)** on a car trip. |
| **Capacity Factor** | The percentage of the year the system produces at full rated power (usually 18% to 24% because the sun goes down at night and clouds exist). | Like a student studying 5 hours out of a 24-hour day ($5 / 24 \approx 21\%$). |
| **IRA Section 6417 ("Direct Pay")** | A federal law that gives tax-exempt entities (like public schools) cash checks from the IRS instead of tax write-offs. | Before 2022, only people who owed taxes got a refund. Now, the government gives schools an **upfront rebate check** regardless of taxes. |
| **Commercial Tariff ($/kWh)** | The retail rate the school pays the utility company for each unit of electricity. | In California (PG&E), it's high (~$0.34/kWh). In Texas, it's lower (~$0.12/kWh). Higher rates mean solar saves more money! |
| **Simple Payback Period** | How many years of electric bill savings it takes to pay off the net installation cost. | If you buy a $100 bicycle that saves you $25/month on bus fares, your payback is 4 months. |
| **Title I School** | A federal designation for schools where at least 40% of students come from low-income families. | Qualifies for an **extra +10% cash bonus** from the IRS to promote climate equity. |
| **Energy Community** | An area that previously relied on coal mines or closed coal plants. | Qualifies for an **extra +10% cash bonus** from the IRS to help workers transition to clean jobs. |

---

## 4. Top 12 Tough Judge Questions & Winning Answers

### Q1: "Did you write this code yourself, and how does it work?"
> **Answer:** *"Yes! I built the application in Python using Streamlit for the user interface, GeoPandas and Folium for the geospatial mapping, and Plotly for the interactive charts. The core computational logic is split into four clean modules: `data_ingest` for school coordinates, `solar_engine` for calling the federal PVWatts API, `financial_model` for IRA Direct Pay and 25-year cashflows, and `report_generator` for compiling the downloadable markdown action brief."*

### Q2: "Why parking lot canopies instead of putting solar panels on the school roof?"
> **Answer:** *"Rooftops sound easy, but in practice they are a nightmare for school facilities directors. High school roofs are covered in bulky HVAC units, have strict weight and seismic limitations, and if a contractor drills mounting bolts through the roof, it often voids the school's 20-year roof warranty. Parking lots have zero roof penetration, unobstructed flat southern exposure, and they provide shade that drops asphalt surface temperatures by over 30°F while protecting student and teacher cars."*

### Q3: "School is out during June and July. Isn't that when solar generates the most power? Is that energy wasted?"
> **Answer:** *"That's a common misconception, but none of it is wasted! Under California's Net Billing Tariff (NEM 3.0 / Solar Billing Plan) and standard commercial interconnection rules across other states, any excess electricity the school generates in the summer is exported back to the grid for utility bill credits. Furthermore, many high schools host summer school, athletic camps, and community programs during peak heat months, so cooling loads remain high."*

### Q4: "Canopies cost more than standard ground mounts or roof mounts ($3.10/W vs $2.20/W). Is it still worth it?"
> **Answer:** *"Yes, because parking lot canopies utilize land the school already owns. Ground-mounted solar requires acres of dedicated open land that schools don't have (or would have to take away from sports fields). Even with the structural steel premium of $3.10 per watt, the 30% to 50% IRS cash check brings the net cost down to around $1.50 to $1.80 per watt, yielding a rapid 3-to-8 year payback."*

### Q5: "How does a public school get money from the IRS if it doesn't file a tax return?"
> **Answer:** *"Under IRS Treasury Decision 9988 issued in March 2024, tax-exempt entities complete a two-step process: First, the school district does an electronic **Pre-Filing Registration** on the IRS portal to receive a registration number for the project. Second, they file **IRS Form 990-T** with Form 3468 attached. The IRS processes the return and issues an electronic direct deposit or paper check directly to the school district's bank account."*

### Q6: "What happens if the Department of Energy PVWatts API goes down during your demo?"
> **Answer:** *"I built resilience into the architecture. In `core/solar_engine.py`, the function tries the live DOE endpoint first. If it encounters a network timeout or rate limit, it automatically switches to an empirical regional fallback based on National Solar Radiation Database constants—1,650 kWh/kW for the Sunbelt, 1,460 for temperate zones, and 1,320 for the north. The app never crashes."*

### Q7: "How did you calibrate your numbers to make sure they are realistic?"
> **Answer:** *"In Phase 1, I calibrated our spatial density factor (0.65) and yield numbers against real, completed solar canopy projects in Silicon Valley—specifically the Cupertino Union School District's 5.2 MW rollout and Fremont Union High School District's canopies at Monta Vista High. Our modeled 1,450 to 1,550 kWh/kW-yr closely matches their published utility data."*

### Q8: "Who pays for routine maintenance and panel cleaning?"
> **Answer:** *"Our 25-year financial model includes an ongoing Operations & Maintenance (O&M) expense line item parameterized at **$15 per kilowatt per year**, escalating at 2% annual inflation. That covers annual robotic brush cleaning, electrical inverter servicing, and monitoring software."*

### Q9: "What is the difference between Phase 1, Phase 2, and Phase 3?"
> **Answer:** *"It's a structured scaling strategy:  
> - **Phase 1 (Bay Area):** Focused locally on 9 counties with PG&E's Schedule B-19 tariff to ground-truth our formulas against real schools.  
> - **Phase 2 (California Statewide):** Expanded to all 58 counties and 10,000 schools using the California Dept of Education directory and CalEnviroScreen equity overlays.  
> - **Phase 3 (Nationwide USA):** Scaled across all 50 states using the federal NCES database of 100,000 schools, state EIA tariffs, and federal IRA Direct Pay bonuses."*

### Q10: "Can these canopies support electric school buses and EV charging?"
> **Answer:** *"Absolutely. That's one of the biggest co-benefits. We included a Level 2 EV charging slider in the app. Parking canopies are already wired with trench conduit and transformers, making it trivial to add Level 2 charging ports for teachers during the day and electric school buses overnight."*

### Q11: "What does EPA eGRID do in your project?"
> **Answer:** *"EPA eGRID gives us the exact carbon intensity of the power grid in each region. For example, in California where the grid is cleaner, avoided emissions are around 0.45 lbs of CO2 per kWh. In Ohio or the Midwest where coal is still used, avoided emissions are over 1.10 lbs of CO2 per kWh. That means a solar canopy in Ohio actually avoids more carbon than the same canopy in California!"*

### Q12: "If you win this hackathon, what is your next step?"
> **Answer:** *"My goal is to pilot this tool directly with our local student climate clubs and the Silicon Valley Youth Climate Action network. We want student delegates to bring these generated Action Briefs to their local school board meetings this winter to advocate for real clean energy canopy resolutions."*

---

## 5. Five-Minute Pre-Pitch Checklist

Before you walk up to present to the judges:
- [ ] Connect your laptop to Wi-Fi.
- [ ] In terminal, run: `streamlit run app.py` and make sure `http://localhost:8501` is open.
- [ ] Select **"Phase 1: Bay Area"** and show **Palo Alto High School** or **Monta Vista High School** (local ground truth).
- [ ] Switch to **"Phase 3: Nationwide USA"** and pick **Westlake High School (Austin, Texas)** to prove national scalability.
- [ ] Point to the top KPI cards: Canopy Capacity $\rightarrow$ Annual Power $\rightarrow$ IRS Direct Pay Check $\rightarrow$ Annual Savings $\rightarrow$ Payback Years.
- [ ] Click **Tab 5 ("School Board Action Brief")** and show the **"Download Executive Action Brief"** button.
- [ ] Smile, take a deep breath, and remember: **You know this data and this tool better than anyone in the room!**
