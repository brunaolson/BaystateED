# Baystate Health Pediatric ED Visualization Tool

Interactive multi-tab visualization tool for Pediatric Emergency Room shift scheduling, census analysis, and operational insights at Baystate Health.

## Live Demo

- **Primary**: [olsonj-wps.github.io/er-shift-visualization](https://olsonj-wps.github.io/er-shift-visualization)
- **Mirror**: [brunaolson.github.io/BaystateED](https://brunaolson.github.io/BaystateED)

## Overview

This tool provides four integrated views for understanding ED operations:

| Tab | Purpose |
|-----|---------|
| **Schedule** | Waterfall shift visualization with patient distribution |
| **Insights** | Key findings, patient flow patterns, and census percentiles |
| **Analysis** | Horizontal timeline correlating census, shifts, and workload |
| **Deep Dive** | Seasonal comparisons, day-of-week variation, and provider variability |

---

## Tab 1: Schedule

### Features
- **Waterfall Chart**: Shifts cascade down as they start (7am-7am cycle)
- **Hover Interactions**: Patient counts per hour for each provider
- **Three-Phase Distribution Model**: Realistic frontloading of patient volume
- **Math Transparency**: Expandable section explaining rate calculations
- **Pediatric Toggle**: Show/hide Pediatric Residents overlay

### Patient Distribution Model

| Phase | Duration | Rate | Description |
|-------|----------|------|-------------|
| High | First 6 hours | 1.5x base | Provider fresh, high productivity |
| Tapering | Middle hours | 0.5x base | Slowing down |
| Wind-down | Final 1-1.5h | 0 | Completing existing cases |

### Shift Schedule

**EM Shifts (Always Visible)**

| Shift | Time | Duration | Patients |
|-------|------|----------|----------|
| Resident #1 | 7am - 4pm | 9h | 13 |
| AP #1 | 9am - 6pm | 9h | 16 |
| Resident #2 | 3pm - 12am | 9h | 13 |
| Flex Attending | 3:30pm - 12am | 8.5h | 18 |
| AP #2 | 5pm - 2am | 9h | 16 |
| Resident #3 | 10pm - 7am | 9h | 13 |

**Pediatric Shifts (Toggle)**

| Shift | Time | Duration | Patients |
|-------|------|----------|----------|
| Peds Intern #1 | 11am - 8pm | 9h | 4 |
| Peds Intern #2 | 1pm - 10pm | 9h | 4 |
| Peds Senior | 11pm - 8am | 9h | 6 |

---

## Tab 2: Insights

### Key Findings Cards
- **Peak Census**: Maximum census time and value
- **Minimum Census**: Lowest census point
- **Peak Arrivals**: Hour with most patient arrivals
- **Plateau Period**: Extended high-census period

### Visualizations
- **Patient Flow**: Arrivals vs Discharges + Admits by hour
- **Census Percentiles**: P25/P50/P75/P95 bands throughout the day
- **ED Coverage**: Total providers and patients by hour

---

## Tab 3: Analysis

Horizontal timeline view showing:

- **Census Overlay**: Bar chart of census throughout the day
- **Shift Swim Lanes**: Visual representation of all active shifts
- **Load Indicator**: Color-coded workload (Low/Moderate/High/Critical)
- **Metric Cards**: Glowing accent cards for key stats

### Load Categories

| Level | Patients/Provider | Color |
|-------|-------------------|-------|
| Low | < 3.5 | Green |
| Moderate | 3.5 - 5.0 | Yellow |
| High | 5.0 - 6.5 | Orange |
| Critical | > 6.5 | Red |

---

## Tab 4: Deep Dive

Uses data from the **Baystate Pediatric ED Staffing Summit** (2024) to provide:

### Winter vs Summer Comparison
Side-by-side hourly census bars showing seasonal variation

### Day of Week APP Coverage
Bar chart showing APP hour variation Monday-Sunday

### Waiting Room Patterns
Hourly waiting room census with P95 overlay

### Provider Variability
Encounter distribution (P10/P50/P90) by provider type:
- MD: Wide variability (24-122 patients)
- APP: Moderate variability (11-38 patients)
- Resident: Moderate variability (18-69 patients)

---

## Data Sources

The Deep Dive tab uses CSV data from the **Baystate Pediatric ED Staffing Summit (2024)**:

| File | Contents |
|------|----------|
| `ped_ed_hourly_7pm_format.csv` | Hourly census, arrivals, discharges, admits, WR census |
| `ped_ed_day_of_week.csv` | APP hours and coverage by day |
| `ped_ed_staffing_variability.csv` | Provider encounter percentiles |

### Data Structure

**Hourly Data Columns:**
```
hour, hour_24, sequence, shift, shift_detail, census_mean, census_median,
census_p25, census_p75, census_p95, wr_census_mean, wr_census_p95,
arrivals_mean, arrivals_p95, discharge_mean, discharge_p95, admit_mean,
admit_p95, lwbs_mean, lwbs_p95, boarding_mean, winter_census, summer_census
```

---

## Files

| File | Description |
|------|-------------|
| `index.html` | Main application (standalone, no build process) |
| `baystate-logo.png` | Baystate Health logo |
| `README.md` | This documentation |

---

## Development

### Architecture

Single-file HTML application with embedded CSS and JavaScript. No external dependencies or build process required.

### Key Functions

| Function | Purpose |
|----------|---------|
| `calculateDistribution(patients, duration, isFlexAttending)` | Three-phase patient distribution |
| `getPatientsAtHour(hour)` | Active providers and patient counts |
| `buildShifts()` | Render Schedule tab waterfall |
| `buildAnalysisTab()` | Render Analysis tab timeline |
| `buildExperimentalTab()` | Render Deep Dive tab visualizations |
| `switchTab(tabId)` | Tab navigation with lazy loading |
| `showTimeTooltip()` / `showShiftTooltip()` | Tooltip handlers |

### Tab Lazy Loading

Tabs are built on first view to improve initial load time:
```javascript
function switchTab(tabId) {
    // ... tab switching logic
    if (tabId === 'analysis' && !analysisBuilt) {
        buildAnalysisTab();
        analysisBuilt = true;
    }
    if (tabId === 'experimental' && !experimentalBuilt) {
        buildExperimentalTab();
        experimentalBuilt = true;
    }
}
```

### Color Palette

| Element | Color |
|---------|-------|
| Residents | Purple (#9b59b6) |
| Advanced Practitioners | Blue (#3498db) |
| Flex Attending | Green (#27ae60) |
| Pediatric Residents | Orange (#e67e22) |
| Census bars | Cyan (#00d4ff) |
| Arrivals | Green (#4ade80) |
| Discharges | Orange (#fb923c) |
| Waiting Room | Magenta (#ff00ff) |

### Extending the Tool

1. **Add new tab**: Create tab button, content div, and `buildNewTab()` function
2. **Add new chart**: Use existing CSS classes (`.chart-bar`, `.chart-container`)
3. **Add new data**: Embed in `buildExperimentalTab()` or load via fetch

---

## Deployment

### GitHub Pages

Both repos auto-deploy from `main` branch:

```bash
# Push to primary
git push origin main

# Push to mirror (requires brunaolson auth)
gh auth switch --user brunaolson
git push bruna main:main
```

### Git Remotes

| Remote | Repository |
|--------|------------|
| origin | github.com/olsonj-wps/er-shift-visualization |
| bruna | github.com/brunaolson/BaystateED |

---

## License

Internal use - Baystate Health / WPS
