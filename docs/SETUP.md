# Development Environment Setup

Local development environment for the Baystate Pediatric ED Visualization project.

---

## System Info

| Component | Detail |
|-----------|--------|
| **Platform** | macOS (Darwin 22.6.0) |
| **Python** | 3.9.6 (system) |
| **Node.js** | 24.14.1 LTS (via nvm) |
| **npm** | 11.11.0 |
| **pip** | 21.2.4 |

---

## Installed Python Packages

### Data Analysis & Spreadsheets

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.3.3 | DataFrames, CSV/Excel analysis |
| numpy | 2.0.2 | Numerical computing |
| scipy | 1.13.1 | Statistical analysis |
| openpyxl | 3.1.5 | Read/write Excel (.xlsx) |
| xlsxwriter | 3.2.9 | Write Excel with formatting |
| xlrd | 2.0.2 | Read legacy Excel (.xls) |
| tabulate | 0.9.0 | Pretty-print tables |

### Visualizations

| Package | Version | Purpose |
|---------|---------|---------|
| matplotlib | 3.9.4 | Static charts and plots |
| seaborn | 0.13.2 | Statistical visualizations |
| plotly | 6.6.0 | Interactive web-based charts |
| bokeh | 3.4.3 | Interactive dashboards |

### PDF & Document Processing

| Package | Version | Purpose |
|---------|---------|---------|
| pdfplumber | 0.11.8 | Extract text/tables from PDFs |
| PyPDF2 | 3.0.1 | PDF manipulation |
| camelot-py | 1.0.9 | Extract tables from PDFs |
| python-docx | 1.2.0 | Read/write Word documents |

### Web & Scraping

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.32.5 | HTTP requests |
| beautifulsoup4 | 4.14.3 | HTML/XML parsing |
| flask | 3.1.3 | Local dev server |
| lxml | 6.0.2 | Fast XML/HTML parser |
| cssutils | 2.11.1 | CSS parsing and validation |

### Scheduling & Calendar

| Package | Version | Purpose |
|---------|---------|---------|
| icalendar | 6.3.2 | Parse/create iCal files (ShiftAdmin exports) |
| python-dateutil | 2.9.0 | Date parsing and manipulation |

### Images & Computer Vision

| Package | Version | Purpose |
|---------|---------|---------|
| Pillow | 11.3.0 | Image processing |
| opencv-python-headless | 4.12.0 | Computer vision (PDF table detection) |

---

## Node.js (via nvm)

Managed with [nvm](https://github.com/nvm-sh/nvm). To activate:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

---

## GitHub Authentication

- **Method**: Personal Access Token (PAT) stored in `.env`
- **Scope**: `repo` (full repository access)
- **Remote**: `origin` -> `https://github.com/brunaolson/BaystateED.git`

The `.env` file is gitignored and never committed.

---

## ShiftAdmin Integration

ShiftAdmin does not have a public API. Data can be ingested via:

1. **CSV/Excel exports** - Parse with pandas
2. **iCal exports** - Parse with icalendar
3. **PDF reports** - Extract with pdfplumber or camelot-py

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/brunaolson/BaystateED.git
cd BaystateED

# Open the visualization directly
open index.html

# Or serve locally with Python
python3 -m http.server 8000
# Then visit http://localhost:8000

# Run data analysis scripts (when available)
python3 scripts/analyze.py
```

---

## Project Structure

```
BaystateED/
├── index.html          # Main standalone visualization app
├── baystate-logo.png   # Baystate Health logo
├── README.md           # Project overview & documentation
├── .env                # GitHub token (gitignored)
├── .gitignore          # Ignored files
└── docs/
    └── SETUP.md        # This file - dev environment docs
```
