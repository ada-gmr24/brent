# Imports:
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # avoiding kernel crashes
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Initialising directories:
experiments_path = Path(__file__).resolve().parent
figures_path = experiments_path / "figures"
figures_path.mkdir(parents=True, exist_ok=True)
data_path = experiments_path.parent / "data" / "along-track-residuals"

satellites = {
    "LAGEOS-1": "lageos1",
    "LAGEOS-2": "lageos2",
    "Etalon 1": "etalon1",
    "Etalon 2": "etalon2",
}

# Create four vertically stacked subplots:
fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)
for ax, (name, folder) in zip(axes, satellites.items()):
    # Load along-track errors:
    df = pd.read_csv(data_path / f"{folder}_along_track_2025.csv")
    dates = pd.to_datetime(df["epoch_utc"])
    along_track = df["along_track_km"]
    # Plotting along-track errors:
    ax.plot(dates, along_track, color="grey", linewidth=0.6, alpha=0.7)
    ax.set_title(name, fontsize=11)
    ax.set_ylabel(r"$\Delta r_{s}$ [km]")
    ax.grid(alpha=0.25)
    ax.axhline(0, color="blue", linewidth=0.5)

# Six date labels:
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
axes[-1].xaxis.set_major_locator(mdates.MonthLocator(bymonth=months))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
axes[-1].tick_params(axis="x", rotation=45)  # rotate 45 degrees
for label in axes[-1].get_xticklabels():
    label.set_horizontalalignment("right")
# No padding between year boundaries and figure border
axes[-1].set_xlim(
    pd.Timestamp("2025-01-01"),
    pd.Timestamp("2026-01-01")
)
axes[-1].set_xlabel("Epoch [-]")
plt.tight_layout()

# Save the figure
output_path = figures_path / "along_track_2025.png"
plt.savefig(output_path, dpi=200)
plt.close()

print(f"Plot saved to: {output_path}")
