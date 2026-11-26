# Imports:
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# File paths:
repo_path = Path(__file__).resolve().parent.parent
data_path = repo_path / "data"
fig_path = Path(__file__).resolve().parent / "figures"
fig_path.mkdir(parents = True, exist_ok = True)

# Load mean + osculating orbital elements:
mean = pd.read_csv(data_path / "mean-elements" / "lageos1_mean_2025.csv", parse_dates=["epoch_utc"])
osc = pd.read_csv(data_path / "osc-elements" / "lageos1_osc_2025.csv", parse_dates=["epoch_utc"])
df = mean.merge(osc, on="epoch_utc").sort_values("epoch_utc")  # match hourly timestamps
# Plotting duration:
df = df[(df["epoch_utc"] >= "2025-01-01") & (df["epoch_utc"] < "2025-02-01")]

# Columns to plot: secular, long-period, osculating, filename
plots = {
    "Semimajor axis [km]": ("a_mean_km", "a_mean_km", "a_osc_km", "a_lageos1.png"),
    "Eccentricity": ("e_mean", "e_lunisolar", "e_osc", "e_lageos1.png"),
    "Inclination [deg]": ("i_mean_deg", "i_lunisolar_deg", "i_osc_deg", "i_lageos1.png"),
    "RAAN [deg]": ("raan_mean_deg", "raan_lunisolar_deg", "raan_osc_deg", "raan_lageos1.png"),
    "Argument of periapsis [deg]": ("omega_mean_deg", "omega_lunisolar_deg", "omega_osc_deg", "omega_lageos1.png")
}

# Generate plots:
for title, (secular, long_period, osculating, filename) in plots.items():
    fig, ax = plt.subplots(figsize=(11, 8))
    for column, label, colour, style, width, alpha, order in [
        (osculating, "Osculating", "lightpink", "-", 0.8, 0.7, 1),
        (secular, "Secular updates", "indigo", "-", 1.5, 1.0, 3),
        (long_period, "Long-period updates", "deeppink", "--", 1.5, 1.0, 4)
    ]:
        y = df[column].copy()
        if "_deg" in column:  # Avoid lines jumping between 0 and 360 degrees
            y = y.mask(y.diff().abs() > 180)
        ax.plot(
            df["epoch_utc"],
            y,
            label=label,
            color=colour,
            linestyle=style,
            linewidth=width,
            alpha=alpha,
            zorder=order
        )

    ax.set_title(f"LAGEOS-1: {title}")
    ax.set_xlabel("Epoch (UTC)")
    ax.set_ylabel(title)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(fig_path / filename, dpi=180)
    plt.close(fig)

print(f"Saved {len(plots)} figures to: {fig_path}")
