# Data Retrieval

This document describes how to retrieve precise satellite orbit data from NASA's [Crustal Dynamics Data Information System (CDDIS)](https://cddis.nasa.gov/) and legacy Two-Line Element sets (TLEs) from [Space-Track](www.space-track.org) using the applications and files provided in the BRENT repository.

These datasets were used to evaluate satellite orbit propagation and
estimation methods against precise reference trajectories for, for example, the four following Medium Earth Orbit (MEO) satellites:

| Satellite | NORAD ID | SP3 Identifier |
| --------- | ---------------- | -------------- |
| LAGEOS-1 | 8820 | L51 |
| LAGEOS-2 | 22195 | L52 |
| Etalon 1 | 19751 | L53 |
| Etalon 2 | 20026 | L54 |


## CDDIS Precise Orbital Data

### Overview

[CDDIS](https://cddis.nasa.gov/) is a NASA data archive supporting space geodesy i.e., the study of the Earth's geometry, gravity, and spatial orientation in 3-D space. It provides a platform for sharing observational data products from techniques such as Global Navigation Satellite Systems (GNSS) and Satellite Laser Ranging
(SLR).

>**Note:** For the LAGEOS and Etalon satellites explored in this repository, precise orbit products are obtained from CDDIS SLR observations.

### SP3 Data Format

Standard Product 3 (SP3) is a standardised format for storing precise satellite ephemerides.

Unlike TLEs, which contain mean orbital elements for use with the SGP4 propagator, SP3 files provide satellite positions at specified epochs, with optional velocity and clock information. This can include:

- Satellite identifiers.
- Observation/solution epochs and associated time-system information.
- Satellite position coordinates.
- Optional satellite velocity and clock information.
- Reference-frame and other product metadata.

>**Note:** For the SLR products considered in this work, orbital data is obtained over 7-day observation arcs and distributed as SP3 files (`.sp3.gz`).

### Configuring CDDIS Downloads

The CDDIS retrieval application is located in:

- [`apps/cddis/`](../apps/cddis/): Application entry point and workflow.
- [`brent/download/cddis.py`](../brent/download/cddis.py): HTTP download implementation.

Download parameters are specified in [`input/cddis.json.example`](../input/cddis.json.example), where the configuration contains:

| Parameter | Description |
| --------- | ----------- |
| `username` | NASA Earthdata account username. |
| `password` | NASA Earthdata account password. |
| `filename_template` | Template for constructing SP3 filenames. |
| `url_root_template` | CDDIS archive URL template. |
| `providers` | ILRS analysis centres supplying orbit solutions (e.g., `esa`). |
| `name` | Satellite name used in the archive (e.g., `lageos1`). |
| `start` | First requested product date (`YYYY-MM-DD`). |
| `end` | Last requested product date (`YYYY-MM-DD`). |
| `frequency` | Interval between requested dates, in days. |
| `output_directory` | Local directory for downloaded files. |

>CDDIS reorganised its SLR archive in October 2026, such that the directory structure for terrestrial-reference-frame orbit products is now:
>
>`/slr/products/orbits/TRF/satellite/YYYY/YYMMDD/`
>
>For the 2025 products considered here, the confirmed filename version is `v80`. The corresponding configuration templates are:
>
>```json
>"filename_template": "${provider}.orb.${name}.${y}${m}${d}.v80.sp3.gz",
>"url_root_template": "https://cddis.nasa.gov/archive/slr/products/orbits/TRF/${name}/${Y}/${y}${m}${d}/"
>```

### Running CDDIS Downloader

Intructions for running the CDDIS downloader and enabling automated data retrieval is provided below:

1. Activate the project's Conda environment.
2. Open `input/cddis.json.example`.
3. Enter valid NASA Earthdata credentials.
4. Specify the satellite, date range, provider and output directory.
5. From the repository root, execute:

```bash
python main.py cddis input/cddis.json.example
```

For example, to retrieve LAGEOS-1 orbit products, configure:

```json
"name": "lageos1",
"start": "2025-01-01",
"end": "2025-12-31",
"frequency": 7,
"output_directory": "./download/lageos1/"
```


## Two-Line Element (TLE) Data

### Overview

Two-Line Element (TLE) sets are a representation of a satellite's orbital state using its mean orbital elements as well as additional parameters. TLEs are designed to be made compatible with the Simplified General Perturbations 4 (SGP4) orbit propagator.

Unlike precise SP3 orbit solutions, TLEs are not precise time-series records of satellite positions, as they provide the parameters required to generate _predicted_ satellite positions and velocities at specified times using SGP4.

[Space-Track](https://www.space-track.org/) is a platform that provides public access to satellite catalogue data and legacy element sets.


### Configuring Space-Track Downloads

The Space-Track retrieval application is located in:

- [`apps/space_track/`](../apps/space_track/): Application implementation.
- [`brent/download/space_track.py`](../brent/download/space_track.py): Downloading functionality.

Download parameters are specified in [`input/space_track.json.example`](../input/space_track.json.example), where the configuration contains:

| Parameter | Description |
| --------- | ----------- |
| `username` | Space-Track account username. |
| `password` | Space-Track account password. |
| `identifiers` | NORAD catalog numbers of the requested satellites. |
| `start` | Start of the requested historical interval. |
| `end` | End of the requested historical interval. |
| `output_directory` | Local destination for downloaded data. |

For example, a 2025 dataset can be configured such that:

```json
{
  "username": "<Space-Track username>",
  "password": "<Space-Track password>",
  "identifiers": [8820, 22195, 19751, 20026],
  "start": "2025-01-01",
  "end": "2025-12-31",
  "output_directory": "./download/tle/"
}
```

Unlike the CDDIS configuration, multiple satellites can be
specified in the `identifiers` array.

### Running the Space-Track Downloader

Intructions for running the Space-Track downloader and enabling automated data retrieval is provided below:

1. Open `input/space_track.json.example`.
2. Enter valid Space-Track credentials.
3. Specify the satellite identifiers and required date range.
4. From the repository root, run:

```bash
python main.py space_track input/space_track.json.example
```

## Data Organisation and Verification

The repository distinguishes between downloaded files and datasets used by the analysis scripts:

| Directory | Purpose |
| --------- | ------- |
| `download/` | Raw data retrieved from CDDIS and Space-Track. |
| [`data/sp3/`](../data/sp3/) | SP3 orbit data used by analysis workflows. |
| [`data/tle/`](../data/tle/) | TLE data used by propagation and fitting workflows. |

Note that the `download/` directory is created by the CDDIS application when required, and is therefore not part of the original repository tree and is unrelated to the [`brent/download`](../brent/download/) directory.
