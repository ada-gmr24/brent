# Imports:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

# Paths:
experiments_path = Path(__file__).resolve().parent
data_path = experiments_path.parent / "data"
comparison_path = data_path / "sgp4mods-comparison"
figures_path = experiments_path / "figures"
figures_path.mkdir(parents=True, exist_ok=True)

# Load SP3 reference states:
sp3 = pd.read_csv(
    data_path / "states" / "lageos1_sp3_2025.csv",
    parse_dates=["epoch_utc"]
)

# Load SGP4 baseline and Hujsak states:
baseline = pd.read_csv(
    comparison_path / "lageos1_sgp4_baseline_2025.csv",
    parse_dates=["epoch_utc"]
)

hujsak = pd.read_csv(
    comparison_path / "lageos1_hujsak_nominal_cx_2025.csv",
    parse_dates=["epoch_utc"]
)

# Calculate along-track residuals (SP3 - SGP4):
r_sp3 = sp3[["x_m", "y_m", "z_m"]].to_numpy()

def calculate_along_track(df):
    r = df[["x_m", "y_m", "z_m"]].to_numpy()
    v = df[["vx_m_s", "vy_m_s", "vz_m_s"]].to_numpy()

    # SGP4-defined RSW frame:
    i_r = r / np.linalg.norm(r, axis=1)[:, None]
    h = np.cross(r, v)
    i_w = h / np.linalg.norm(h, axis=1)[:, None]
    i_s = np.cross(i_w, i_r)

    # Along-track residual in km:
    delta_r = r_sp3 - r
    return np.sum(delta_r * i_s, axis=1) * 0.001

along_baseline = calculate_along_track(baseline)
along_hujsak = calculate_along_track(hujsak)

# Plot both models:
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    sp3["epoch_utc"], along_baseline,
    color="indigo", linewidth=0.8,
    label="SGP4 baseline"
)

ax.plot(
    sp3["epoch_utc"], along_hujsak,
    color="deeppink", linewidth=0.8,
    label=r"Hujsak (nominal $C_X$)"
)

ax.set_title("LAGEOS-1: SGP4 Baseline vs Hujsak")
ax.set_ylabel(r"$\Delta r_s$ [km]")
ax.set_xlabel("Epoch [-]")
ax.axhline(0, color="gray", linewidth=0.5)
ax.grid(alpha=0.25)
ax.legend()

# Date formatting:
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.tick_params(axis="x", rotation=45)
ax.set_xlim(pd.Timestamp("2025-01-01"), pd.Timestamp("2026-01-01"))

plt.tight_layout()

# Save figure:
output_file = figures_path / "lageos1_baseline_vs_hujsak_2025.png"
plt.savefig(output_file, dpi=200)
plt.close()

print(f"Plot saved to: {output_file}")
