# Imports:
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Repo paths:
data_path = Path.cwd().resolve().parent / "data"
download_path = Path.cwd().resolve().parent / "download"
fig_path = Path(__file__).resolve().parent / "figures"
fig_path.mkdir(parents = True, exist_ok = True)

# Load LAGEOS-2 TLEs:
tles = pd.read_json(download_path / "tle" / "22195.json")
for col in ["EPOCH", "CREATION_DATE"]:
    tles[col] = pd.to_datetime(tles[col], utc=True).dt.tz_localize(None)
tles = (tles.sort_values(["EPOCH", "CREATION_DATE"]).drop_duplicates("EPOCH", keep="last"))

# Load along-track residuals:
res = pd.read_csv(data_path / "along-track-residuals" / "lageos2_along_track_2025.csv",
    parse_dates=["epoch_utc"])
res["epoch_utc"] = pd.to_datetime(res["epoch_utc"], utc=True).dt.tz_localize(None)

# Match each residual to the latest preceding TLE epoch:
df = pd.merge_asof(res.sort_values("epoch_utc"),
    tles[["EPOCH", "CREATION_DATE"]].sort_values("EPOCH"), left_on="epoch_utc",
    right_on="EPOCH",direction="backward")
df["tle_age_days"] = (df["epoch_utc"] - df["EPOCH"]).dt.total_seconds()/86400

# Plotting:

dates = df["epoch_utc"]
t = (dates - dates.iloc[0]).dt.total_seconds().to_numpy()/86400
sinusoid = 0.55 * np.sin(2*np.pi*t/13.15 + np.deg2rad(-45))  # approximated sinusoid
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True, gridspec_kw={"height_ratios": [1, 1]})

# Top Panel: Along-track residuals
ax1.plot(dates, df["along_track_km"], color="lightpink", linewidth=0.6, alpha=0.7, label="Along-track residual")
ax1.plot(dates, sinusoid, color="deeppink", linewidth=1.5, label="Approximate sinusoid")
ax1.axhline(0, color="indigo", linewidth=0.5)
ax1.set_title("LAGEOS-2", fontsize=11)
ax1.set_ylabel(r"$\Delta r_s$ [km]")
ax1.grid(alpha=0.25)

# Bottom Panel: TLE Ages
usage = df.groupby("EPOCH", as_index=False)["tle_age_days"].max()  # max. age of TLEs
ax2.bar(usage["EPOCH"], usage["tle_age_days"], width=2, color="indigo", alpha=0.85, zorder=3)
ax2.set_ylim(0, usage["tle_age_days"].max() * 1.20)  # create headroom for second panel
for _, row in usage[usage["tle_age_days"] >= 15].iterrows():  # label bars > 15 days
    ax2.annotate(f'{row["tle_age_days"]:.0f} days', xy=(row["EPOCH"], row["tle_age_days"]),
        xytext=(0, 8), textcoords="offset points", ha="center", fontsize=14, fontweight="medium")
ax2.plot(
    tles["CREATION_DATE"], np.zeros(len(tles)), "|", color="indigo", markersize=7, label="TLE creation dates")
ax2.set_ylabel("Max. TLE Age [days]")
ax2.set_xlabel("Epoch [-]")
ax2.set_ylim(bottom=0)
ax2.grid(alpha=0.25)

# Plot Formatting:

months = list(range(1, 13))
ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=months))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax2.tick_params(axis="x", rotation=45)
for label in ax2.get_xticklabels():
    label.set_horizontalalignment("right")
# Exact 2025 boundaries, without additional padding
ax2.set_xlim(pd.Timestamp("2025-01-01"), pd.Timestamp("2026-01-01"))
for ax in (ax1, ax2):
    ax.tick_params(axis="both", labelsize=11)
    ax.yaxis.label.set_size(13)
ax1.set_title("LAGEOS-2", fontsize=15)
ax2.xaxis.label.set_size(13)
ax2.tick_params(axis="x", labelsize=11, rotation=45)
fig.tight_layout()
fig.subplots_adjust(hspace=0.00)  # space between panels

# Save:
fig.savefig(fig_path / "residuals_creation_lageos2_2025.png", dpi=200)
plt.close(fig)
