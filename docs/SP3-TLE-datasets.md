# Downloaded Datasets

This document summarises the satellite orbital datasets retrieved for [experimental work](../experiments/) in this repository spanning the 2025 analysis period. This data will be used to investigate orbit propagation accuracy for four Medium Earth Orbit (MEO) satellites.

## Overview

Two types of orbital data have been acquired:
- **Precise SP3 ephemerides:** Obtained from NASA's Crustal Dynamics Data Information System (CDDIS), using orbit solutions derived from Satellite Laser Ranging (SLR) observations.
- **Two-Line Element (TLEs) sets:** Obtained from Space-Track, providing SGP4-compatible mean orbital elements for satellite propagation.

The inventory for satellite orbital data covering both SP3 and TLE datasets are as follows:

| Satellite | NORAD ID | SP3 Files | Legacy TLEs |
| --------- | -------- | --------- | ---------------------- |
| LAGEOS-1 | 8820 | 52 | 659 |
| LAGEOS-2 | 22195 | 52 | 398 |
| Etalon 1 | 19751 | 52 | 603 |
| Etalon 2 | 20026 | 52 | 644 |
| **Total** | 4 | **208** | **2304** |

## Datasets

### 1. Precise SP3 Orbit Data

The source of SP3 files is the [NASA CDDIS](https://cddis.nasa.gov/) database, where ILRS precise orbit solutions (`ilrsa`, version `v80`) can be obtained in a Gzip-compressed SP3 (`.sp3.gz`) format. The analysis period selected was from January 1st to December 31st 2026, where the retrieved SP3 file dates were January 4th to December 27th 2025 at 7-day intervals (52 files per satellite).

The SP3 products contain precise satellite ephemerides derived from SLR observations and are intended to serve as reference trajectories for subsequent propagation comparisons.

>**Note:** The dates above describe the requested weekly product dates, not the exact temporal coverage of the orbit states within each SP3 file.

### 2. TLE Data

The source of TLE datasets is [Space-Track](https://www.space-track.org/), where legacy TLEs can be obtained from historical General Perturbations element sets (`gp_history`). Via the Brent repository, JSON files containing orbital element records, including `TLE_LINE1` and `TLE_LINE2`, are retrieved automatically. The requested period of TLE retrieval for four MEO satellites was January 1st to December 31st 2025.

| Satellite | TLE Records | First Epoch (UTC) | Last Epoch (UTC) |
| --------- | ----------- | ----------------- | ---------------- |
| LAGEOS-1 | 659 | 2025-01-01 03:21:13 | 2025-12-30 13:50:31 |
| LAGEOS-2 | 398 | 2025-01-06 12:31:12 | 2025-12-11 16:31:48 |
| Etalon 1 | 603 | 2025-01-01 16:41:27 | 2025-12-30 07:47:35 |
| Etalon 2 | 644 | 2025-01-01 08:56:40 | 2025-12-30 09:35:25 |
| **Total** | **2,304** | - | - |

>**Note:** The available TLE epochs are not uniformly spaced, particularly as LAGEOS-2 also has a shorter retrieved epoch range than the other satellites. This should be considered when defining subsequent analysis intervals.

## Data Retrieval and Reproducibility

Both datasets were retrieved using the existing download applications within the Brent repository.

| Dataset | Configuration | Application |
| ------- | ------------- | ----------- |
| SP3 | [`input/cddis.json.example`](../input/cddis.json.example) | [`apps/cddis/`](../apps/cddis/) |
| TLE | [`input/space_track.json.example`](../input/space_track.json.example) | [`apps/space_track/`](../apps/space_track/) |

See [Data Retrieval](data-retrieval.md) for instructions on retrieving these datasets. The raw downloaded files are currently retained in `download/`, where the repository's experimental analyses will expect prepared data under `data/sp3/` and `data/tle/`.

