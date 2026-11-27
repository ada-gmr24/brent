# Imports:
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

def plot_along_track_comparison(
    sp3_path,
    baseline_path,
    modified_path,
    output_file,
    title,
    labels=("SGP4 baseline", "Modified SGP4"),
    colors=("indigo", "deeppink"),
    xlim=None,
    ylim=None,
    xlabel="Epoch [-]",
    ylabel=r"$\Delta r_s$ [km]",
    figsize=(12, 5),
    linewidth=0.8,
    dpi=200,
    date_format="%Y-%m",
    month_interval=1,
    rotation=45,
    legend_loc="best",
    grid_alpha=0.25,
    zero_color="gray",
    zero_linewidth=0.5,
):
    sp3 = pd.read_csv(sp3_path, parse_dates=["epoch_utc"])
    position_columns = ["x_m", "y_m", "z_m"]
    velocity_columns = ["vx_m_s", "vy_m_s", "vz_m_s"]
    r_sp3 = sp3[position_columns].to_numpy()

    def calculate_along_track(df):
        # Match the SP3 timestamps and their order:
        df = df.set_index("epoch_utc").loc[sp3["epoch_utc"]]
        r = df[position_columns].to_numpy()
        v = df[velocity_columns].to_numpy()
        i_r = r / np.linalg.norm(r, axis=1)[:, None]
        h = np.cross(r, v)
        i_w = h / np.linalg.norm(h, axis=1)[:, None]
        i_s = np.cross(i_w, i_r)

        return np.sum((r_sp3 - r) * i_s, axis=1) * 0.001

    # Use Agg directly so plotting does not open a GUI window:
    fig = Figure(figsize=figsize)
    FigureCanvasAgg(fig)
    ax = fig.subplots()

    for path, label, color in (
        (baseline_path, labels[0], colors[0]),
        (modified_path, labels[1], colors[1]),
    ):
        df = pd.read_csv(path, parse_dates=["epoch_utc"])
        ax.plot(sp3["epoch_utc"], calculate_along_track(df),
            color=color, linewidth=linewidth, label=label,)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.axhline(0, color=zero_color, linewidth=zero_linewidth)
    ax.grid(alpha=grid_alpha)
    ax.legend(loc=legend_loc)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=month_interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    ax.tick_params(axis="x", rotation=rotation)

    if xlim is not None:
        ax.set_xlim(pd.to_datetime(xlim))
    if ylim is not None:
        ax.set_ylim(ylim)

    fig.tight_layout()
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_file, dpi=dpi)
    return output_file