"""
generate_derived.py
Reads raw CSVs from /Users/brunaolson/BaystateED/data/ and produces
derived datasets in /Users/brunaolson/BaystateED/data/derived/
"""

import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/brunaolson/BaystateED/data"
DERIVED_DIR = "/Users/brunaolson/BaystateED/data/derived"
os.makedirs(DERIVED_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Helper: pivot hourly census data into {category: {metric: series}}
# ---------------------------------------------------------------------------
def load_hourly_census(path):
    df = pd.read_csv(path)
    # Returns a dict keyed by (category, metric) -> Series indexed by hour
    pivot = df.pivot_table(index="hour", columns=["category", "metric"],
                           values="value", aggfunc="first")
    return pivot


# ===========================================================================
# 1. net_flow_winter.csv  &  net_flow_summer.csv
# ===========================================================================
def build_net_flow(season):
    path = os.path.join(DATA_DIR, f"hourly_census_{season}.csv")
    df = pd.read_csv(path)

    def get_series(cat, met):
        sub = df[(df["category"] == cat) & (df["metric"] == met)].copy()
        sub = sub.sort_values("hour").set_index("hour")["value"]
        return sub.reindex(range(24)).fillna(0)

    arrivals_mean  = get_series("arrivals",  "mean")
    discharge_mean = get_series("discharge", "mean")
    admit_mean     = get_series("admit",     "mean")

    net_flow = arrivals_mean - discharge_mean - admit_mean
    cumulative = net_flow.cumsum()

    out = pd.DataFrame({
        "hour":               range(24),
        "arrivals_mean":      arrivals_mean.values,
        "discharges_mean":    discharge_mean.values,
        "admits_mean":        admit_mean.values,
        "net_flow":           net_flow.values,
        "cumulative_net_flow": cumulative.values,
    })

    out_path = os.path.join(DERIVED_DIR, f"net_flow_{season}.csv")
    out.to_csv(out_path, index=False)
    print(f"net_flow_{season}.csv  -> {len(out)} rows")


build_net_flow("winter")
build_net_flow("summer")


# ===========================================================================
# 2. demand_vs_capacity.csv
# ===========================================================================
def build_demand_vs_capacity():
    rows = []

    for season in ["winter", "summer"]:
        census_path   = os.path.join(DATA_DIR, f"hourly_census_{season}.csv")
        staffing_path = os.path.join(DATA_DIR, f"staffing_analysis_{season}.csv")

        census_df   = pd.read_csv(census_path)
        staffing_df = pd.read_csv(staffing_path)

        def census_val(cat, met, h):
            sub = census_df[(census_df["category"] == cat) &
                            (census_df["metric"]   == met) &
                            (census_df["hour"]     == h)]
            return float(sub["value"].iloc[0]) if len(sub) else np.nan

        # Staffing capacity: sum capacity_pph across non-TOTAL rows per hour
        # (TOTAL row already summarises but using individual rows avoids double-count)
        staff_detail = staffing_df[staffing_df["shift_name"] != "TOTAL"].copy()
        # capacity per provider per hour * attending_shifts = patients/hour for that slot
        staff_detail = staff_detail.copy()
        staff_detail["slot_capacity"] = (
            staff_detail["attending_shifts"] * staff_detail["capacity_pph"]
        )
        hourly_cap = (
            staff_detail.groupby("hour")["slot_capacity"]
            .sum()
            .reindex(range(24))
            .fillna(0)
        )

        # patients_per_provider: total capacity / total attending shifts
        total_shifts = (
            staffing_df[staffing_df["shift_name"] == "TOTAL"]
            .set_index("hour")["attending_shifts"]
            .reindex(range(24))
            .fillna(0)
        )

        for h in range(24):
            c_mean  = census_val("census", "mean", h)
            c_p95   = census_val("census", "p95",  h)
            wr_mean = census_val("wr",     "mean", h)
            wr_p95  = census_val("wr",     "p95",  h)
            cap     = hourly_cap[h]
            ts      = total_shifts[h]
            ppp     = round(cap / ts, 4) if ts > 0 else np.nan

            rows.append({
                "hour":               h,
                "season":             season,
                "census_mean":        c_mean,
                "census_p95":         c_p95,
                "wr_mean":            wr_mean,
                "wr_p95":             wr_p95,
                "staffing_capacity":  round(cap, 4),
                "patients_per_provider": ppp,
                "demand_gap":         round(c_mean - cap, 4) if not np.isnan(c_mean) else np.nan,
                "demand_gap_p95":     round(c_p95 - cap, 4) if not np.isnan(c_p95) else np.nan,
            })

    out = pd.DataFrame(rows)
    out_path = os.path.join(DERIVED_DIR, "demand_vs_capacity.csv")
    out.to_csv(out_path, index=False)
    print(f"demand_vs_capacity.csv -> {len(out)} rows")


build_demand_vs_capacity()


# ===========================================================================
# 3. rotation_risk_scores.csv
# ===========================================================================
def build_rotation_risk_scores():
    df = pd.read_csv(os.path.join(DATA_DIR, "capacity_28day_hourly.csv"))

    # Derive total_capacity from existing capacity columns
    # total_patient_capacity_9h is already in units of patients/provider-hour;
    # reconstruct absolute daily capacity as sum of individual capacities
    df["total_capacity"] = (
        df["junior_capacity"] +
        df["senior_capacity"] +
        df["fellow_capacity"] +
        df["app_capacity"]
    )

    cap_mean = df["total_capacity"].mean()
    cap_std  = df["total_capacity"].std()

    def risk(cap):
        if cap < cap_mean - cap_std:
            return "high"
        elif cap < cap_mean:
            return "medium"
        else:
            return "low"

    out = df[["day", "total_provider_hours", "total_capacity",
              "junior_hours", "senior_hours", "fellow_hours", "app_hours"]].copy()

    out["risk_score"]          = out["total_capacity"].apply(risk)
    out["capacity_vs_mean_pct"] = (
        (out["total_capacity"] - cap_mean) / cap_mean * 100
    ).round(2)

    out_path = os.path.join(DERIVED_DIR, "rotation_risk_scores.csv")
    out.to_csv(out_path, index=False)
    print(f"rotation_risk_scores.csv -> {len(out)} rows")


build_rotation_risk_scores()


# ===========================================================================
# 4. seasonal_comparison.csv
# ===========================================================================
def build_seasonal_comparison():
    categories = ["census", "wr", "arrivals", "discharge", "admit", "lwbs", "boarding"]
    metrics    = ["mean", "p95"]

    winter_df = pd.read_csv(os.path.join(DATA_DIR, "hourly_census_winter.csv"))
    summer_df = pd.read_csv(os.path.join(DATA_DIR, "hourly_census_summer.csv"))

    def lookup(df, cat, met):
        sub = df[(df["category"] == cat) & (df["metric"] == met)].copy()
        sub = sub.sort_values("hour").set_index("hour")["value"]
        return sub.reindex(range(24))

    rows = []
    for cat in categories:
        for met in metrics:
            w = lookup(winter_df, cat, met)
            s = lookup(summer_df, cat, met)
            for h in range(24):
                wv = w[h] if not pd.isna(w[h]) else np.nan
                sv = s[h] if not pd.isna(s[h]) else np.nan
                diff = round(wv - sv, 4) if not (np.isnan(wv) or np.isnan(sv)) else np.nan
                pct  = round((wv - sv) / sv * 100, 2) if (
                    not (np.isnan(wv) or np.isnan(sv)) and sv != 0
                ) else np.nan
                rows.append({
                    "hour":         h,
                    "category":     cat,
                    "metric":       met,
                    "winter_value": wv,
                    "summer_value": sv,
                    "difference":   diff,
                    "pct_change":   pct,
                })

    out = pd.DataFrame(rows)
    out_path = os.path.join(DERIVED_DIR, "seasonal_comparison.csv")
    out.to_csv(out_path, index=False)
    print(f"seasonal_comparison.csv -> {len(out)} rows")


build_seasonal_comparison()


# ===========================================================================
# 5. app_optimization.csv
# ===========================================================================
def build_app_optimization():
    coverage = pd.read_csv(os.path.join(DATA_DIR, "coverage_hours.csv"))

    # Identify APP shifts – coverage_hours has shift_name and hours per day-of-week
    # The file lists all shifts for attending coverage; there is no explicit APP flag.
    # According to the capacity_28day_hourly data, APPs contribute app_hours.
    # In coverage_hours the shifts are: Day, Mid-Day, Evening, Swing, Night (winter)
    #                                   Day, Evening, Swing, Night (summer)
    # There is no APP-specific shift listed in coverage_hours.csv.
    # Strategy: use capacity_28day_hourly.csv to get average APP hours by day-of-week
    # (days 1-28 map to weeks; day % 7 gives day-of-week index 0-6 -> Mon-Sun).

    cap28 = pd.read_csv(os.path.join(DATA_DIR, "capacity_28day_hourly.csv"))

    # Map day 1-28 to day-of-week (0=Mon ... 6=Sun), assuming day 1 = Monday
    cap28["dow_idx"]    = (cap28["day"] - 1) % 7
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cap28["day_of_week"] = cap28["dow_idx"].map(lambda i: day_names[i])

    app_by_dow = (
        cap28.groupby("day_of_week")["app_hours"]
        .mean()
        .reindex(day_names)
        .reset_index()
        .rename(columns={"app_hours": "current_app_hours"})
    )

    # Census peak: use winter + summer combined; take the max mean census hour value
    # as a proxy for daily peak, averaged across days of week (no per-dow census data,
    # so use the single overall peak census mean across all 24 hours for all days).
    winter_census = pd.read_csv(os.path.join(DATA_DIR, "hourly_census_winter.csv"))
    summer_census = pd.read_csv(os.path.join(DATA_DIR, "hourly_census_summer.csv"))

    w_peak = (
        winter_census[(winter_census["category"] == "census") &
                      (winter_census["metric"]   == "mean")]["value"].max()
    )
    s_peak = (
        summer_census[(summer_census["category"] == "census") &
                      (summer_census["metric"]   == "mean")]["value"].max()
    )
    # Use average of the two seasons as a reasonable overall daily peak
    overall_peak = (w_peak + s_peak) / 2

    PPH = 2.5  # target patients per provider hour

    app_by_dow["census_mean_peak"]          = overall_peak
    app_by_dow["target_hours_at_2_5_pph"]   = round(overall_peak / PPH, 2)
    app_by_dow["gap"] = (
        app_by_dow["target_hours_at_2_5_pph"] - app_by_dow["current_app_hours"]
    ).round(2)

    out_path = os.path.join(DERIVED_DIR, "app_optimization.csv")
    app_by_dow.to_csv(out_path, index=False)
    print(f"app_optimization.csv    -> {len(app_by_dow)} rows")


build_app_optimization()

print("\nAll derived files written to", DERIVED_DIR)
