# Contributing to SolarSchools USA

Thank you for your interest in contributing to SolarSchools USA. This project is dedicated to democratizing clean energy finance and geospatial solar planning for K-12 public schools across America. Whether you are a high school student climate advocate, an educator, a software engineer, or a renewable energy professional, your contributions are welcome.

---

## Code of Conduct

All contributors and participants agree to abide by the [Code of Conduct](./CODE_OF_CONDUCT.md). We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone.

---

## How to Get Involved

You can contribute to SolarSchools USA in several ways:

1. **Adding School Campuses:** Expand our school database with verified parking lot coordinates, local utility tariffs, and enrollment figures.
2. **Improving Physical & Financial Models:** Enhance solar generation calculations, EV charging load profiles, battery storage sizing, or state-specific tariff modeling.
3. **Enhancing the Web Interface:** Improve Streamlit visualization, interactive mapping, responsiveness, and accessibility.
4. **Documentation & Advocacy Materials:** Refine presentation guides, school board template resolutions, and user tutorials.
5. **Bug Reports & Feature Requests:** Submit detailed issues describing bugs or proposing improvements.

---

## Development Setup

### Prerequisites

* Python 3.10 or higher
* Git

### Step-by-Step Installation

1. Fork the repository on GitHub and clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/svyca2026.git
   cd svyca2026
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify your setup by running the test suite:
   ```bash
   python test_pipeline.py
   ```

5. Launch the Streamlit development dashboard:
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## Adding New School Campuses

Campus data is maintained in [`core/data_ingest.py`](./core/data_ingest.py) under the `SCHOOL_DATABASE` dictionary. When adding a new school, ensure all fields follow this schema:

```python
"School Name (City, State)": {
    "phase": "Phase 1: Bay Area",  # or "Phase 2: California Statewide", "Phase 3: Nationwide USA"
    "level": "High School",        # "Elementary School", "Middle School", or "High School"
    "district": "Full District Name",
    "county": "County Name",
    "state": "Two-Letter State Code",
    "lat": 37.1234,               # Exact coordinates of the main parking lot
    "lon": -122.1234,
    "enrollment": 1800,
    "utility": "Utility Name (Tariff Schedule)",
    "commercial_tariff": 0.345,   # Blended rate in $/kWh
    "default_lot_m2": 7500,       # Paved parking footprint in square meters
    "is_title1": False,           # True if Title I federal qualification applies
    "energy_community": False,    # True if located in an IRA Energy Community
    "solar_status": "Unshaded (Losing Money)",  # or "Implemented (Active Savings)"
    "installed_year": None,
    "deployment_details": "Clear summary of canopy feasibility or existing array."
}
```

### Coordinate Verification Standard

Always ground-truth parking lot coordinates using satellite imagery (e.g., Google Maps or OpenStreetMap). The latitude and longitude must point directly to the paved vehicular parking surface, not the school administration building or athletic field.

---

## Coding Standards

* **Python Style:** Follow PEP 8 conventions. Use 4 spaces for indentation.
* **Type Annotations:** Include Python type hints for all function arguments and return values.
* **Docstrings:** Document all modules, classes, and public functions with clear docstrings.
* **Documentation Tone:** Keep documentation objective, technical, and data-backed. Do not include emojis in source code or markdown documents.
* **SPDX Headers:** Include the standard copyright and SPDX license identifier header in all new Python source files:
  ```python
  # SolarSchools USA
  # Copyright (c) 2026 Pranav Balaji
  # SPDX-License-Identifier: MIT
  ```

---

## Testing & Verification

Before submitting any code changes, execute the test suite:

```bash
python test_pipeline.py
```

All tests must pass with an exit code of 0. If you introduce new computational logic, add corresponding unit test cases to [`test_pipeline.py`](./test_pipeline.py).

---

## Commit Guidelines

We follow Conventional Commits format for git commit messages:

* `feat:` A new user-facing feature or calculation module
* `fix:` A bug fix in calculations, mapping, or UI
* `docs:` Documentation updates (markdown files, docstrings)
* `refactor:` Code improvements without behavioral changes
* `test:` Adding or updating unit tests
* `chore:` Build process, dependency updates, or repository maintenance

Example:
```bash
git commit -m "feat(solar_engine): add temperature derate factor for Central Valley campuses"
```

---

## Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/add-oakland-unified
   ```
2. Make your edits and commit following the guidelines above.
3. Push your branch to your GitHub fork:
   ```bash
   git push origin feat/add-oakland-unified
   ```
4. Open a Pull Request against the `main` branch.
5. In your PR description, describe:
   - What changes were made and why.
   - Any data sources used with verifiable links.
   - Confirmation that `python test_pipeline.py` passed cleanly.
