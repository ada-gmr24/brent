# Imports:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

# Paths (notebook-friendly):
repo_path = Path.cwd().resolve()
if repo_path.name == "experiments":
    experiments_path = repo_path
    repo_path = repo_path.parent
else:
    experiments_path = repo_path / "experiments"

data_path = repo_path / "data"
comparison_path = data_path / "sgp4mods-comparison"
figures_path = experiments_path / "figures"
figures_path.mkdir(parents=True, exist_ok=True)

# Load SP3 reference states:
sp3 = pd.read_csv(
    data_path / "states" / "lageos1_sp3_2025.csv",
    parse_dates=["epoch_utc"]
)

# Load the 3 SGP4 model outputs:
baseline = pd.read_csv(
    comparison_path / "lageos1_sgp4_baseline_2025.csv",
    parse_dates=["epoch_utc"]
)

hujsak_nominal = pd.read_csv(
    comparison_path / "lageos1_hujsak_nominal_cx_2025.csv",
    parse_dates=["epoch_utc"]
)

hujsak_full = pd.read_csv(
    comparison_path / "lageos1_hujsak_full_cx_2025.csv",
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
along_nominal = calculate_along_track(hujsak_nominal)
along_full = calculate_along_track(hujsak_full)

# Plot all 3 on separate panels:
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

series = [
    (along_baseline, "indigo", "SGP4 baseline"),
    (along_nominal, "deeppink", r"Hujsak (nominal $C_X$)"),
    (along_full, "teal", r"Hujsak (full $C_X$)")
]

for ax, (y, colour, title) in zip(axes, series):
    ax.plot(
        sp3["epoch_utc"], y,
        color=colour, linewidth=0.8
    )
    ax.set_title(f"LAGEOS-1: {title}")
    ax.set_ylabel(r"$\Delta r_s$ [km]")
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.grid(alpha=0.25)

# Date formatting:
axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
axes[-1].tick_params(axis="x", rotation=45)
axes[-1].set_xlim(pd.Timestamp("2025-01-01"), pd.Timestamp("2026-01-01"))
axes[-1].set_xlabel("Epoch [-]")

plt.tight_layout()

# Save figure:
output_file = figures_path / "lageos1_baseline_nominal_full_cx_2025.png"
plt.savefig(output_file, dpi=200)
plt.close()

print(f"Plot saved to: {output_file}")