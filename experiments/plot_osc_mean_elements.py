# Imports:
from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Directories:
experiments_path = Path(__file__).resolve().parent
data_path = experiments_path.parent / "data"
figures_path = experiments_path / "figures"
figures_path.mkdir(parents = True, exist_ok = True)

# Choosing start and end plotting date:
start_date = "2025-01-01"
end_date = "2025-02-01"  # excluded
start = pd.Timestamp(start_date)
end = pd.Timestamp(end_date)

# Load mean and osculating elements:
mean_df = pd.read_csv(data_path / "mean-elements" / "lageos1_mean_2025.csv", parse_dates=["epoch_utc"])
mean_df = mean_df[(mean_df["epoch_utc"] >= start) & (mean_df["epoch_utc"] < end)]  # clip to start:end
osc_df = pd.read_csv(data_path / "osc-elements" / "lageos1_osc_2025.csv",parse_dates=["epoch_utc"])
osc_df = osc_df[(osc_df["epoch_utc"] >= start) & (osc_df["epoch_utc"] < end)]

# Define + plot all orbital elements:
elements = {
    "a": ("Semimajor axis", "km", "a_mean_km", "a_osc_km"),
    "e": ("Eccentricity", "", "e_mean", "e_osc"),
    "i": ("Inclination", "deg", "i_mean_deg", "i_osc_deg"),
    "raan": ("RAAN", "deg", "raan_mean_deg", "raan_osc_deg"),
    "omega": ("Argument of periapsis", "deg", "omega_mean_deg", "omega_osc_deg"),
    "theta": ("True anomaly", "deg", "theta_mean_orbit_deg", "theta_osc_deg"),
}

for symbol, (name, unit, mean_col, osc_col) in elements.items():
    fig, ax = plt.subplots(figsize=(12, 6))
    # Use points for angular elements to avoid 360-degree wrap lines:
    if symbol in ["raan"]:  # angles
        ax.scatter(osc_df["epoch_utc"], osc_df[osc_col], color="deeppink", s=2,
            label="Osculating")
        ax.scatter(mean_df["epoch_utc"], mean_df[mean_col], color="indigo", s=5,
            label="TLE mean")
    else:  # non-angular
        ax.plot(osc_df["epoch_utc"], osc_df[osc_col], color="deeppink", linewidth=0.7,
            alpha=0.7, label="Osculating")
        ax.plot(mean_df["epoch_utc"], mean_df[mean_col], color="indigo", linewidth=1.2,
            label="TLE mean")

    # Formatting:
    ax.set_title(f"LAGEOS-1: {name}")
    ax.set_ylabel(f"{name} [{unit}]" if unit else name)  # iterate over elements
    ax.set_xlabel("Epoch")
    ax.grid(alpha=0.25)
    ax.legend(loc = "best")
    # fixing x-labels
    #month_interval = 2 if (end - start).days > 180 else 1
    #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=month_interval))
    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    day_interval = 2
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=day_interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    # Forcing start - end date for x-axis
    ax.set_xlim(start, end)
    ax.margins(x=0)
    fig.tight_layout()

    # Saving/exporting figures:
    output_path = figures_path / f"{symbol}_lageos1.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
