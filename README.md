# ER Shift Coverage Visualization

Interactive waterfall-style visualization tool for Pediatric Emergency Room shift scheduling at Baystate Health.

## Overview

This tool visualizes 24-hour ER shift coverage (7am to 7am) showing:
- **EM Shifts**: Residents, Advanced Practitioners (APs), and Flex Attending
- **Pediatric Overlay**: Optional toggle to show Pediatric Residents coverage

## Features

- **Waterfall Chart**: Shifts cascade down as they start throughout the day
- **Hover Interactions**: See expected patient counts per hour for each provider
- **Three-Phase Distribution Model**: Realistic frontloading of patient volume
- **Math Transparency**: Expandable section explaining all rate calculations
- **Baystate Health Branding**: Official colors and logo

## Patient Distribution Model

Patients are distributed across each shift in three phases:

| Phase | Duration | Rate | Description |
|-------|----------|------|-------------|
| High | First 6 hours | 1.5× base | Provider is fresh, higher productivity |
| Tapering | Middle hours | 0.5× base | Slowing down |
| Wind-down | Final 1h (1.5h for Flex) | 0 | Completing existing cases, no new patients |

### Example: 9-hour Resident Shift (13 patients)

```
Equation: 13 = 6(1.5X) + 2(0.5X) + 1(0)
          13 = 9X + 1X = 10X
          X = 1.3 (base rate)

First 6h:  1.95 pts/hr × 6h = 11.7 pts
Middle 2h: 0.65 pts/hr × 2h = 1.3 pts
Final 1h:  0 pts/hr × 1h    = 0 pts
                       Total: 13 pts ✓
```

## Shift Schedule

### EM Shifts (Always Visible)

| Shift | Time | Duration | Patients |
|-------|------|----------|----------|
| Resident #1 | 7am - 4pm | 9h | 13 |
| AP #1 | 9am - 6pm | 9h | 16 |
| Resident #2 | 3pm - 12am | 9h | 13 |
| Flex Attending | 3:30pm - 12am | 8.5h | 18 |
| AP #2 | 5pm - 2am | 9h | 16 |
| Resident #3 | 10pm - 7am | 9h | 13 |

### Pediatric Shifts (Toggle On/Off)

| Shift | Time | Duration | Patients |
|-------|------|----------|----------|
| Peds Intern #1 | 11am - 8pm | 9h | 4 |
| Peds Intern #2 | 1pm - 10pm | 9h | 4 |
| Peds Senior | 11pm - 8am | 9h | 6 |

## Usage

1. Open `index.html` in a web browser
2. Hover over any time slot on the left to see patient counts for that hour
3. Hover over any shift block to see that provider's distribution
4. Click "Show Pediatric Residents" to toggle the overlay
5. Expand "How are rates calculated?" for detailed math

## Color Legend

| Provider Type | Color |
|---------------|-------|
| Residents | Purple |
| Advanced Practitioners | Blue |
| Flex Attending | Green |
| Pediatric Residents | Orange |

## Files

- `index.html` - Main visualization (standalone, no dependencies)
- `baystate-logo.png` - Baystate Health logo
- `README.md` - This documentation

## Development

This is a standalone HTML file with no build process or dependencies. Edit `index.html` directly.

### Key Functions

- `calculateDistribution(patients, duration, isFlexAttending)` - Calculates three-phase patient distribution
- `getPatientsAtHour(hour)` - Returns all active providers and their patient counts for a given hour
- `buildShifts()` - Renders shift blocks on the chart
- `showTimeTooltip()` / `showShiftTooltip()` - Tooltip handlers

## License

Internal use - Baystate Health / WPS
