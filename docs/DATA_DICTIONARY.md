# PEM Staffing Summit Data Dictionary

**Source file:** `PEM Staffing Summit Data_3.22.26 (2).xlsx`
**Data period:** FY 2024/25 — October 2024/2025 through September 2025/2026
**Parsed by:** `data/parse_pem_data.py`
**Output directory:** `data/`
**Last updated:** 2026-03-30

---

## Overview

This dataset captures Pediatric Emergency Medicine (PEM) census, staffing, and capacity data at Baystate Medical Center. It is organized by season:

- **Winter (FW / Oct-Mar):** October 2024/2025 – March 2025/2026
- **Summer (SS / Apr-Sept):** April 2024/2025 – September 2024/2025

Data comes from 10 Excel sheets, each serving a different analytical purpose. The parsed CSVs are all in **long format** (one observation per row) to maximize downstream usability in Python, R, or any BI tool.

---

## Output CSV Files

### 1. `hourly_census_winter.csv`

**Source sheet:** `FW` (Fall/Winter clean summary)
**Rows:** 1,152 (8 categories × 6 metrics × 24 hours)
**Description:** Rounded/summary statistics for the winter season by hour of day. Use for quick analysis and visualization.

| Column     | Type    | Description |
|------------|---------|-------------|
| `category` | string  | Clinical measure (see Category Codes below) |
| `metric`   | string  | Statistical measure (see Metric Codes below) |
| `hour`     | integer | Hour of day, 0–23 (0 = midnight, 12 = noon) |
| `value`    | numeric | Rounded value for the given category/metric/hour combination |

---

### 2. `hourly_census_summer.csv`

**Source sheet:** `SS` (Spring/Summer clean summary)
**Rows:** 1,152
**Description:** Same structure as `hourly_census_winter.csv` but for the summer season.

Same columns as `hourly_census_winter.csv`.

---

### 3. `hourly_census_raw_winter.csv`

**Source sheet:** `Oct-Mar`
**Rows:** 1,152
**Description:** Full-precision (6 decimal places) values for the winter season. Use when exact statistical values matter (e.g., for formal reports, regression inputs, or comparing small differences between seasons).

| Column     | Type    | Description |
|------------|---------|-------------|
| `category` | string  | Clinical measure (see Category Codes) |
| `metric`   | string  | Statistical measure (see Metric Codes) |
| `hour`     | integer | Hour of day, 0–23 |
| `value`    | numeric | Full-precision float (e.g., 22.802857 instead of 23) |

---

### 4. `hourly_census_raw_summer.csv`

**Source sheet:** `Apr-Sept`
**Rows:** 1,152
**Description:** Full-precision values for the summer season. Same structure as `hourly_census_raw_winter.csv`.

---

#### Category Codes (used in census CSVs)

| Code           | Full Name in Excel                        | Clinical Meaning |
|----------------|-------------------------------------------|------------------|
| `census`       | Total Pedi ED Census                      | Total patients physically present in the ED at that hour |
| `wr`           | WR Census                                 | Patients in the waiting room (not yet in a bed) |
| `boarding`     | Crisis/Bedsearch Boarding Census          | Psychiatric/boarding patients awaiting inpatient bed |
| `arrivals`     | ED Hourly New Arrival                     | New patients arriving per hour |
| `bed_assignment` | ED Hourly New Bed Assignment            | Patients assigned to a treatment bed per hour |
| `discharge`    | ED Hourly Checkout (Discharged Pts)       | Patients discharged home per hour |
| `admit`        | ED Hourly Checkout (Admitted Pts)         | Patients admitted to inpatient per hour |
| `lwbs`         | Count of LWBS based on Arrival Times      | Left Without Being Seen patients per hour |

#### Metric Codes (used in census CSVs)

| Code     | Meaning |
|----------|---------|
| `mean`   | Arithmetic mean across all days in the season |
| `median` | 50th percentile |
| `p25`    | 25th percentile (Q1) |
| `p75`    | 75th percentile (Q3) |
| `p95`    | 95th percentile (near-worst-case) |
| `stdev`  | Standard deviation |

---

### 5. `coverage_hours.csv`

**Source sheet:** `Coverage Hours`
**Rows:** 63
**Description:** Attending physician shift schedule — hours per shift per day of week, for each season.

| Column        | Type    | Description |
|---------------|---------|-------------|
| `season`      | string  | `Oct-Mar` or `Apr-Sept` |
| `shift_name`  | string  | Shift label: `Day`, `Mid-Day` (Oct-Mar only), `Evening`, `Swing`, `Night` |
| `day_of_week` | string  | `Monday` through `Sunday` |
| `hours`       | numeric | Duration of this shift in hours (all shifts = 8.5 h) |

**Notes:**
- Oct-Mar has 5 shifts per day (Day, Mid-Day, Evening, Swing, Night) = 42.5 total hours/day
- Apr-Sept has 4 shifts per day (Day, Evening, Swing, Night) = 34.0 total hours/day
- The Mid-Day shift is a winter-only flex shift

---

### 6. `provider_variability.csv`

**Source sheet:** `Coverage Hours` (rows 1–4)
**Rows:** 15 (3 provider types × 5 percentiles)
**Description:** Distribution of daily hours worked by provider type, expressed as percentiles across the observation period.

| Column          | Type    | Description |
|-----------------|---------|-------------|
| `provider_type` | string  | `MD Hours`, `APP Hours`, or `Resident Hours` |
| `percentile`    | string  | `p10`, `p25`, `p50`, `p75`, `p90` |
| `hours`         | numeric | Daily hours at this percentile |

**Interpretation:** The wide spread (e.g., MD p10=24 vs p90=122) reflects high day-to-day variability in attending physician effort/scheduling.

---

### 7. `staffing_analysis_winter.csv`

**Source sheet:** `FW Analysis`
**Rows:** 144 (24 hours × 6 rows per hour: 5 shifts + 1 TOTAL)
**Description:** Hourly attending physician coverage for the winter schedule. Shows how many attending-shift-equivalents are active in each hour, and the resulting patient capacity (PPH = 2.5 patients per attending per hour).

| Column              | Type    | Description |
|---------------------|---------|-------------|
| `season`            | string  | Always `winter` |
| `hour`              | integer | Hour of day, 0–23 |
| `shift_name`        | string  | Shift identifier (e.g., `Day (7:30a-4p)`) or `TOTAL` |
| `attending_shifts`  | numeric | Fraction of an attending shift active during this hour |
| `capacity_pph`      | numeric | Patient capacity: `attending_shifts × 2.5` for individual shifts; total capacity for `TOTAL` rows |

**Winter shifts:**
- `Day (7:30a-4p)`
- `Flex (11:30a-8p)` — mid-day flex shift
- `Evening (3:30p-12a)`
- `Swing (5p-1:30a)`
- `Night (11:30p-8a)`

**PPH = 2.5** patients per attending per hour (from the Excel model).

---

### 8. `staffing_analysis_summer.csv`

**Source sheet:** `SS Analysis`
**Rows:** 120 (24 hours × 5 rows per hour: 4 shifts + 1 TOTAL)
**Description:** Same structure as `staffing_analysis_winter.csv` but for the summer schedule (no Mid-Day/Flex shift).

**Summer shifts:**
- `Day (7:30a-4p)`
- `Evening (1:30p-10p)`
- `Swing (5p-1:30a)`
- `Night (11:30p-8a)`

---

### 9. `capacity_28day.csv`

**Source sheet:** `Total Capacity Analysis`
**Rows:** 238
**Description:** The 28-day resident/fellow rotation schedule in long format. Each row represents one provider slot assignment for one day of the cycle.

| Column          | Type    | Description |
|-----------------|---------|-------------|
| `day`           | integer | Day of the 28-day rotation cycle (1–28) |
| `slot_position` | integer | Vertical slot in the rotation grid (1 = top row, higher = lower row) |
| `provider_type` | string  | Provider code (see Provider Codes below) |

**Provider Codes:**

| Code  | Full Role |
|-------|-----------|
| `EMS` | Senior Emergency Medicine Resident (EMS track) |
| `EMI` | Junior Emergency Medicine Resident (EMI track) |
| `AP`  | Advanced Practice Provider (APP/NP/PA) |
| `F`   | Fellow |
| `Pi1` | Pediatric Intern 1 (Junior) |
| `Pi2` | Pediatric Intern 2 (Junior) |
| `Ps1` | Pediatric Senior 1 |
| `Ps2` | Pediatric Senior 2 |

**Note:** Multiple rows per day reflect multiple provider slots (e.g., day 1 may have EMS + AP + F + Ps2 + EMI working on that calendar day). The `slot_position` is an artifact of the grid layout and does not imply shift order.

---

### 10. `capacity_28day_hourly.csv`

**Source sheet:** `Total Capacity Analysis` (right-side table)
**Rows:** 28 (one per day of the rotation cycle)
**Description:** Aggregate provider hours and patient capacity for each of the 28 rotation days. "Capacity" here is the number of patients each provider type can see in a 9-hour shift period.

| Column                      | Type    | Description |
|-----------------------------|---------|-------------|
| `day`                       | integer | Day of the 28-day rotation (1–28) |
| `junior_hours`              | numeric | Total junior resident hours scheduled (EMI, Pi) |
| `junior_capacity`           | numeric | Patient capacity from junior residents (hours × 0.25 PPH) |
| `senior_hours`              | numeric | Total senior resident hours (EMS, Ps) |
| `senior_capacity`           | numeric | Patient capacity from seniors (hours × 1.5 PPH) |
| `fellow_hours`              | numeric | Total fellow hours |
| `fellow_capacity`           | numeric | Patient capacity from fellows (hours × 2.0 PPH) |
| `app_hours`                 | numeric | Total APP hours |
| `app_capacity`              | numeric | Patient capacity from APPs (hours × 2.0 PPH) |
| `total_provider_hours`      | numeric | Sum of all provider hours for the day |
| `total_patient_capacity_9h` | numeric | Total estimated patients seen in the 9-hour model period |

**PPH rates used in the Excel model:**
- Junior residents: 0.25 patients/hour
- Senior residents: 1.5 patients/hour
- Fellows: 2.0 patients/hour
- APPs: 2.0 patients/hour

---

### 11. `resident_shifts.csv`

**Source sheet:** `Sheet3`
**Rows:** 28 (one per day of the 28-day rotation)
**Description:** Junior and senior resident shift counts and hours for each day of the rotation cycle.

| Column           | Type    | Description |
|------------------|---------|-------------|
| `day`            | integer | Day of 28-day rotation (1–28) |
| `junior_shifts`  | integer | Number of junior resident shifts scheduled (EMI/Pi) |
| `senior_shifts`  | integer | Number of senior resident shifts scheduled (EMS/Ps) |
| `junior_hours`   | numeric | Total junior resident hours (shifts × 9 h) |
| `senior_hours`   | numeric | Total senior resident hours (shifts × 9 h) |
| `total_shifts`   | integer | Junior + Senior shifts combined |
| `total_hours`    | numeric | Junior + Senior hours combined |

---

### 12. `provider_summary.csv`

**Source sheet:** `Sheet3` (summary table)
**Rows:** 5
**Description:** Summary of average daily coverage by provider category across the 28-day rotation.

| Column                   | Type   | Description |
|--------------------------|--------|-------------|
| `provider_category`      | string | Provider role group |
| `avg_shifts_per_day`     | string | Average shifts scheduled per day (formatted string, e.g., "3.04 Shifts") |
| `avg_hours_per_day`      | string | Average hours scheduled per day (e.g., "27.32 Hours") |
| `pct_of_total_coverage`  | float  | Fraction of total coverage hours (0.0–1.0) |

**Summary values:**

| Provider Category            | Avg Shifts/Day | Avg Hours/Day | % of Coverage |
|------------------------------|---------------|---------------|---------------|
| Senior Residents (EMS, Ps)   | 3.04          | 27.32 h       | 35.8%         |
| Junior Residents (EMI, Pi)   | 2.82          | 25.39 h       | 33.3%         |
| APPs (AP)                    | 2.25          | 20.25 h       | 26.6%         |
| Fellows (F)                  | 0.36          | 3.21 h        | 4.3%          |
| **Total Daily Workforce**    | ~8.46         | 76.18 h       | 100%          |

---

### 13. `graph_data_summer.csv`

**Source sheet:** `Graph Data` (SS section, rows 1–15)
**Rows:** 336
**Description:** Pre-computed visualization data for summer season. Covers arrivals and bed assignments with full statistical distributions and delta calculations.

| Column     | Type    | Description |
|------------|---------|-------------|
| `season`   | string  | Always `summer` |
| `category` | string  | `arrivals` or `bed_assignment` |
| `metric`   | string  | `mean`, `median`, `p25`, `p75`, `p95`, `stdev`, `delta_25%`, `delta_95%` |
| `hour`     | integer | Hour of day, 0–23 |
| `value`    | numeric | Value for this category/metric/hour |

**Delta metrics:** `delta_25%` = P75 - P25 (interquartile spread); `delta_95%` = P95 - P75 (upper tail spread). These are useful for visualizing uncertainty bands in graphs.

---

### 14. `graph_data_winter.csv`

**Source sheet:** `Graph Data` (FW section, rows 17–31)
**Rows:** 336
**Description:** Same structure as `graph_data_summer.csv` but for the winter season.

Same columns as `graph_data_summer.csv`.

---

## Common Usage Patterns

### Load and filter a census file

```python
import pandas as pd

fw = pd.read_csv("data/hourly_census_winter.csv")

# Mean total census by hour
mean_census = fw[(fw.category == "census") & (fw.metric == "mean")]

# All metrics for arrivals
arrivals = fw[fw.category == "arrivals"]
arrivals_wide = arrivals.pivot(index="hour", columns="metric", values="value")
```

### Compare winter vs summer census at peak hour (18:00)

```python
fw = pd.read_csv("data/hourly_census_winter.csv")
ss = pd.read_csv("data/hourly_census_summer.csv")

fw_18 = fw[(fw.hour == 18) & (fw.metric == "mean")][["category","value"]].rename(columns={"value":"winter"})
ss_18 = ss[(ss.hour == 18) & (ss.metric == "mean")][["category","value"]].rename(columns={"value":"summer"})

comparison = fw_18.merge(ss_18, on="category")
```

### Overlay demand vs capacity (winter)

```python
fw_arrivals = pd.read_csv("data/hourly_census_winter.csv")
fw_staffing = pd.read_csv("data/staffing_analysis_winter.csv")

demand = fw_arrivals[(fw_arrivals.category == "arrivals") & (fw_arrivals.metric == "mean")]
supply = fw_staffing[fw_staffing.shift_name == "TOTAL"][["hour","capacity_pph"]]

merged = demand.merge(supply, on="hour")
merged["gap"] = merged["capacity_pph"] - merged["value"]
```

### Analyze 28-day rotation coverage

```python
rotation = pd.read_csv("data/capacity_28day.csv")

# Count provider types per day
coverage = rotation.groupby(["day","provider_type"]).size().unstack(fill_value=0)

# Days with fellow coverage
fellow_days = rotation[rotation.provider_type == "F"]["day"].unique()
```

---

## Data Quality Notes

1. **Rounding in clean summary sheets (FW/SS):** Values in `hourly_census_winter.csv` and `hourly_census_summer.csv` are rounded to whole numbers. Use the `_raw_` variants for exact values.

2. **28-day rotation vs calendar weeks:** The rotation in `capacity_28day.csv` is a cyclical 28-day schedule. It does not directly map to calendar months — multiply through for longer periods.

3. **PPH = 2.5 attending assumption:** The staffing analysis assumes each attending physician sees 2.5 patients per hour. This drives the capacity columns in `staffing_analysis_*.csv`.

4. **APP coverage schedule:** APP hours vary by day of week and are not uniform. The `coverage_hours.csv` captures shift-level structure; detailed APP time-of-day data appears in the original `Coverage Hours` sheet.

5. **Fast Track (Nov–Feb):** An additional Fast Track APP coverage block runs November–February (120 days). Hours from this block are **not** included in the parsed CSVs — they exist in the `Coverage Hours` sheet under the "Fast track" table.

6. **LWBS data:** Left-Without-Being-Seen counts are very low (median = 0 for most hours) and should be interpreted as rare events.

7. **Season definitions:**
   - Winter/FW: October, November, December, January, February, March
   - Summer/SS: April, May, June, July, August, September

---

## File Summary Table

| File                          | Source Sheet            | Rows  | Key Fields |
|-------------------------------|-------------------------|-------|------------|
| `hourly_census_winter.csv`    | FW                      | 1,152 | category, metric, hour, value |
| `hourly_census_summer.csv`    | SS                      | 1,152 | category, metric, hour, value |
| `hourly_census_raw_winter.csv`| Oct-Mar                 | 1,152 | category, metric, hour, value |
| `hourly_census_raw_summer.csv`| Apr-Sept                | 1,152 | category, metric, hour, value |
| `coverage_hours.csv`          | Coverage Hours          | 63    | season, shift_name, day_of_week, hours |
| `provider_variability.csv`    | Coverage Hours          | 15    | provider_type, percentile, hours |
| `staffing_analysis_winter.csv`| FW Analysis             | 144   | season, hour, shift_name, attending_shifts, capacity_pph |
| `staffing_analysis_summer.csv`| SS Analysis             | 120   | season, hour, shift_name, attending_shifts, capacity_pph |
| `capacity_28day.csv`          | Total Capacity Analysis | 238   | day, slot_position, provider_type |
| `capacity_28day_hourly.csv`   | Total Capacity Analysis | 28    | day, *_hours, *_capacity, total_patient_capacity_9h |
| `resident_shifts.csv`         | Sheet3                  | 28    | day, junior_shifts, senior_shifts, *_hours |
| `provider_summary.csv`        | Sheet3                  | 5     | provider_category, avg_shifts_per_day, pct_of_total_coverage |
| `graph_data_summer.csv`       | Graph Data (SS)         | 336   | season, category, metric, hour, value |
| `graph_data_winter.csv`       | Graph Data (FW)         | 336   | season, category, metric, hour, value |
