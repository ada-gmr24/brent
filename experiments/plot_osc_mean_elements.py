
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Run plotting outside Jupyter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# File paths
repo_path = Path(__file__).resolve().parent.parent
data_path = repo_path / "data"

mean_path = data_path / "mean-elements" / "lageos1_mean_2025.csv"
osc_path = data_path / "osc-elements" / "lageos1_osc_2025.csv"

fig_path = Path(__file__).resolve().parent / "figures"
fig_path.mkdir(parents=True, exist_ok=True)


# Load data
mean = pd.read_csv(mean_path, parse_dates=["epoch_utc"])
osc = pd.read_csv(osc_path, parse_dates=["epoch_utc"])

# Match the exact comparison epochs
df = (
    mean.merge(osc, on="epoch_utc", how="inner", validate="one_to_one")
        .sort_values("epoch_utc")
        .reset_index(drop=True)
)

if len(df) != len(mean):
    raise ValueError(
        "The osculating elements do not cover all mean-element epochs. "
        "Recalculate them using the same 15-minute tle_states."
    )

print("Matched comparison epochs:", len(df))


# Colours
SECULAR = "#7566AD"
LONG_PERIOD = "#169E9C"
OSCULATING = "#E56C94"


def break_angle_wraps(values):
    """Prevent lines connecting 360 degrees back to 0 degrees."""
    y = np.asarray(values, dtype=float).copy()
    jumps = np.abs(np.diff(y)) > 180
    y[1:][jumps] = np.nan
    return y


def plot_element(name, ylabel, secular, long_period, osculating,
                 filename, angular=False):

    fig, ax = plt.subplots(figsize=(11, 4.5))

    x = df["epoch_utc"]

    curves = [
        (secular, "Secular mean", SECULAR),
        (long_period, "Secular + long-period", LONG_PERIOD),
        (osculating, "Osculating", OSCULATING)
    ]

    for values, label, colour in curves:
        y = break_angle_wraps(values) if angular else values

        ax.plot(x, y, label=label, color=colour, linewidth=1.1)

    ax.set_title(f"LAGEOS-1: {name}")
    ax.set_xlabel("Epoch (UTC)")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    ax.legend()

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M"))

    fig.tight_layout()
    fig.savefig(fig_path / filename, dpi=180)
    plt.close(fig)


# Five orbital elements
plots = [
    ("Semimajor axis", "a [km]",
     "a_mean_km", "a_mean_km", "a_osc_km",
     "a_lageos1.png", False),

    ("Eccentricity", "e",
     "e_mean", "e_j3_proxy", "e_osc",
     "e_lageos1.png", False),

    ("Inclination", "i [deg]",
     "i_mean_deg", "i_lunisolar_deg", "i_osc_deg",
     "i_lageos1.png", False),

    ("RAAN", "Omega [deg]",
     "raan_mean_deg", "raan_lunisolar_deg", "raan_osc_deg",
     "raan_lageos1.png", True),

    ("Argument of periapsis", "omega [deg]",
     "omega_mean_deg", "omega_j3_proxy_deg", "omega_osc_deg",
     "omega_lageos1.png", True)
]

for name, ylabel, s_col, lp_col, o_col, filename, angular in plots:
    plot_element(
        name, ylabel,
        df[s_col], df[lp_col], df[o_col],
        filename, angular
    )


# Optional sixth plot:
# True anomaly inferred from mean (M, e) using Kepler's equation.
# These are reference-ellipse proxies, NOT fully osculating anomalies.
def kepler_true_anomaly(M_deg, ecc):

    M = np.deg2rad(np.asarray(M_deg, dtype=float)) % (2*np.pi)
    ecc = np.asarray(ecc, dtype=float)

    E = M.copy()

    for _ in range(12):
        E -= (E - ecc*np.sin(E) - M) / (1 - ecc*np.cos(E))

    theta = np.arctan2(
        np.sqrt(1 - ecc**2)*np.sin(E),
        np.cos(E) - ecc
    )

    return np.degrees(theta) % 360


theta_secular = kepler_true_anomaly(
    df["M_mean_deg"], df["e_mean"]
)

theta_long = kepler_true_anomaly(
    df["M_lunisolar_deg"], df["e_j3_proxy"]
)

plot_element(
    "True anomaly (mean-ellipse proxies)",
    "theta [deg]",
    theta_secular,
    theta_long,
    df["theta_osc_deg"],
    "theta_comparison.png",
    angular=True
)

print(f"Saved six figures to: {fig_path}")
