# BRENT

![License](https://img.shields.io/badge/license-BSD--3-D3E6FF)

## Overview

BRENT (Batch Regression for Estimating Noise in TLEs) is a tool under development for conducting pseudo-orbit determination on Two-line Element Sets (TLEs).

## Repository Structure

The table below outlines the main components and usage descriptions offered by BRENT.

| Paths | Description |
| ----- | ----------- |
| [`apps/`](apps/) | Command-line applications for running individual workflows. |
| &nbsp;&nbsp;↳ [`cddis/`](apps/cddis/) | Download precise SP3 orbit products from CDDIS. |
| &nbsp;&nbsp;↳ [`space_track/`](apps/space_track/) | Retrieve orbital element data from Space-Track. |
| &nbsp;&nbsp;↳ [`generate_stles/`](apps/generate_stles/) | Generate synthetic Two-Line Element sets (TLEs). |
| &nbsp;&nbsp;↳ [`sweep/`](apps/sweep/) | Execute parameter-sweep experiments. |
| &nbsp;&nbsp;↳ [`sweep_plot/`](apps/sweep_plot/) | Plot results from parameter-sweep experiments. |
| &nbsp;&nbsp;↳ [`tle_fit/`](apps/tle_fit/) | Run TLE-fitting workflows. |
| &nbsp;&nbsp;↳ [`tle_residuals/`](apps/tle_residuals/) | Analyse and plot TLE residuals. |
| [`brent/`](brent/) | Core Python package containing reusable algorithms and utilities. |
| &nbsp;&nbsp;↳ [`download/`](brent/download/) | Data retrieval modules for [CDDIS](brent/download/cddis.py), [Space-Track](brent/download/space_track.py), and [CelesTrak](brent/download/celestrak.py). |
| &nbsp;&nbsp;↳ [`propagators/`](brent/propagators/) | Orbit propagation implementations, including [analytical](brent/propagators/analytical/), [numerical](brent/propagators/numerical/), and [Vallado SGP4](brent/propagators/vallado_sgp4/) propagators. |
| &nbsp;&nbsp;↳ [`filter/`](brent/filter/) | Orbit estimation and fitting algorithms, including [batch least-squares](brent/filter/batchleastsquares/) and [synthetic TLE filtering](brent/filter/stle.py). |
| &nbsp;&nbsp;↳ [`frames/`](brent/frames/) | Orbital coordinate representations and transformations. |
| &nbsp;&nbsp;↳ [`bias/`](brent/bias/) | Models for representing systematic biases. |
| &nbsp;&nbsp;↳ [`covariance/`](brent/covariance/) | Models for representing estimation uncertainty and covariance. |
| &nbsp;&nbsp;↳ [`io/`](brent/io/) | Input/output handling and data serialisation utilities. |
| &nbsp;&nbsp;↳ [`util/`](brent/util/) | General-purpose utilities and helper functions. |
| [`data/`](data/) | Local datasets and supporting files. |
| [`docs/`](docs/) | Documentation on dataset retrievals. |
| [`experiments/`](experiments/) | Jupyter notebooks with experimental analyses. |
| [`external/`](external/) | External dependencies, including [`thalassa/`](external/thalassa/). |
| [`input/`](input/) | Example JSON configurations for [CDDIS](input/cddis.json.example), [Space-Track](input/space_track.json.example), [synthetic TLE generation](input/stle.json.example), and [parameter sweeps](input/sweep.json.example). |
| [`output/`](output/) | Generated experiment outputs and results. |
| [`environment.yml`](environment.yml) | Conda environment specifying project dependencies. |
| [`main.py`](main.py) | Main command-line entry point, responsible for selecting and executing applications. |

## Data Availability

## Installation

The following command can be used to clone the repository and its submodules:
```
git clone --recurse-submodules https://github.com/maxhlc/brent
```

Alternatively, the submodules can be initialised at a later point:
```
git submodule update --init --recursive
```

An environment file is provided to create a conda environment with all of the required dependencies:

```
conda env create -f environment.yml
conda activate brent
```

## Usage

The main script used with BRENT is `main.py` which is the entry point for various applications in the `./apps/` directory. Many of these use configuration files with examples provided in the `./input/` directory.

TLEs and ILRS/DORIS/IGS orbit product data are expected in JSON and SP3 formats respectively.

#### Orekit
The Python wrappers for Orekit are distributed through the conda package manager. No further configuration should be required to install Orekit.

Orekit requires data files (including physical parameters, reference frame parameters, etc.) which can be obtained from the [Orekit Data repository](https://gitlab.orekit.org/orekit/orekit-data). These are automatically included as a git submodule.

#### THALASSA

THALASSA must be compiled (including its Python bindings) before it can be used by BRENT. THALASSA uses the CMake build system, and can be configured and built with the following commands:
```
cmake -B ./build -S .
cmake --build ./build
```

It is recommended to execute these within the conda environment to ensure that the Python bindings are compatible with the environment's version of Python.

By default, BRENT uses SPICE kernels with THALASSA lunisolar perturbations, therefore the following files must be placed into the `./data/kernels/` directory:
* `de431_part-1.bsp`
* `de431_part-2.bsp`
* `gm_de431.tpc`
* `naif0012.tls`

A script for downloading the kernel files is provided by THALASSA (`./external/thalassa/data/kernels/kernels.sh`).

> **Note**: SPICE kernels are loaded relative to the current working directory, unlike the Orekit data files which are loaded with absolute filepaths.

#### Residuals from a saved TLE fit

Run from the `brent` directory with the `brent` conda environment active:

```
python main.py tle_residuals -i output/20260908_123207
```

The app reads the final single-object `tle_fit` pickle and the original TLE history CSV at the path stored in that result. It propagates the fitted GCRF state forward and backward from the fit epoch, using the fitted beta and saved physical model and tolerance, to every TLE epoch within the saved fit window (inclusive). The original relative TLE path is resolved from the working directory.

The output is `<run>_residuals.csv` in the fit directory; use `-o path/to/residuals.csv` to choose another file. Columns contain UTC epochs, MJD UTC, and the six RIC components of **THALASSA minus TLE**, with position in metres and velocity in m/s. Each TLE is evaluated at its own epoch using the same SGP4 and TEME-to-GCRF conversion as `tle_fit`. RIC axes come from that TLE's osculating state. Both position and velocity differences are rotated onto those axes; velocity columns are inertial velocity differences expressed in RIC, without a rotating-frame derivative term. This residual sign is opposite to the fit's stored `z_final`.

## License
This project is licensed under the MIT License.
