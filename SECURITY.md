# Security Policy

## Supported Versions

We provide security updates and patches for the following versions of SolarSchools USA:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | Yes                |
| < 1.0   | No                 |

---

## Reporting a Vulnerability

The SolarSchools USA team takes the security and integrity of our codebase and community seriously. If you discover a security vulnerability or potential threat within this repository, please report it responsibly.

### Responsible Disclosure Process

1. **Do Not Open a Public Issue:** To protect users and public school partners, please do not file public GitHub issues for security vulnerabilities.
2. **Submit a Private Advisory:** Use GitHub's [Private Vulnerability Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-communicating-vulnerabilities/privately-reporting-a-security-vulnerability) feature on this repository.
3. **Information to Include:**
   * A description of the vulnerability and its potential impact.
   * Clear steps to reproduce the issue (code snippets, terminal commands, or screenshots).
   * Any potential mitigations or suggested fixes you have identified.
4. **Response Timeline:**
   * A project maintainer will acknowledge receipt of your vulnerability report within 48 hours.
   * We will provide regular status updates until a patch is verified and deployed.

---

## External APIs and API Key Handling

SolarSchools USA interacts with external public service endpoints, specifically:

* **U.S. Department of Energy / National Laboratory of the Rockies (NLR) PVWatts v8 REST API**
* **OpenStreetMap Nominatim and Overpass APIs**

### Guidelines for Developers & Deployers

* **No Hardcoded Secrets:** Never commit personal or organizational API keys, access tokens, or private credentials into source code or Git history.
* **Environment Variables:** Always configure API keys using environment variables (e.g., `NLR_API_KEY`).
* **Fallback Resilience:** The application includes built-in regional fallback estimators to operate reliably even without active external API keys.

---

## Data Privacy & Student Records

* **Zero Student PII:** SolarSchools USA does **not** collect, store, or process any Personally Identifiable Information (PII) of students, teachers, or administrators.
* **Public Data Only:** All school records, geographic coordinates, and district utility tariffs are sourced exclusively from public federal directories (NCES, CDE, EIA, EPA).
* **Local Processing:** Financial simulations, cashflow models, and Action Brief documents are processed locally in Python and are not transmitted to third-party tracking servers.
