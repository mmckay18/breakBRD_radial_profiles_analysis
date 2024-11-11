# breakBRD_radial_profiles_analysis

Codebase for creating and analyzing BreakBRD galaxies radial distribution profiles from the SDSS MaNGA survey

# M31 Red Giant Branch Stars Metallicity Distribution Function and Gradient

By Myles McKay(@mmckay18),

![Astronomy](https://img.shields.io/badge/Field-Astronomy-blue)
![Last Commit](https://img.shields.io/github/last-commit/mmckay18/phast_rgbstars_mdf)
![Repo Size](https://img.shields.io/github/repo-size/mmckay18/phast_rgbstars_mdf)
![Contributors](https://img.shields.io/github/contributors/mmckay18/phast_rgbstars_mdf)
![Pull Requests](https://img.shields.io/github/issues-pr/mmckay18/phast_rgbstars_mdf)
![License](https://img.shields.io/github/license/mmckay18/phast_rgbstars_mdf)
![Issues](https://img.shields.io/github/issues/mmckay18/phast_rgbstars_mdf)
![Stars](https://img.shields.io/github/stars/mmckay18/phast_rgbstars_mdf)
![Forks](https://img.shields.io/github/forks/mmckay18/phast_rgbstars_mdf)

# Table of Contents

- [Introduction](#introduction)
- [Research Abstract](#research-abstract)
- [Data](#data) - [Data Sources](#data-sources) - [Data Acquisition](#data-acquisition) - [Data Preprocessing](#data-preprocessing)
- [Results and Evaluation](#results-and-evaluation)
  - [PHAT and PHAST RGB Spatial Metallicity Map](#phat-and-phast-rgb-spatial-metallicity-map)
  - [RGB Metallicity Distribution Function](#rgb-metallicity-distribution-function)
  - [RGB Metallicity Gradient](#rgb-metallicity-gradient)
- [Future Work](#future-work)
- [References](#references)
<!-- - [License](#license) -->

# Introduction

- This repository is made too show the complete workflow for analyzing the 14 distinct galaxies with intresting the star formation distrubiution using integral field unit spectrocopy from the MaNGA survey. I outline the exploratory data analysis, image processing, statistical analysis and data visualization.

# Research Abstract

The spatial distribution of stellar age properties provide key insights into the dynamic evolution of nearby galaxies. Using SDSS-IV MaNGA data, we investigate how the radial stellar age and mass profiles of 11 centrally-concentrated star-forming galaxies with photometrically red disks (Breaking Bulges in Red Disks; BreakBRDs) to examine for differences in the stellar age population distribution on sub-kpc scales. We aim to clarify if the BreakBRD galaxies central stellar population is indeed younger than the disk on the resolved scales and correspond to global measurements from previous literature. We compare the distribution plots to the control parent sample of galaxies with red bulges with photometrically red or blue disks. The parent sample is then separated into centrally star- forming, centrally green-valley and centrally quiescent galaxies based on Dn4000 index as a stellar age indicator. We find that the BreakBRD galaxies show a departure in the stellar age of the outer disk but a similar central stellar age to centrally star-forming galaxies, further indicating that the red outer disk is indeed older than the central region as seen in the global measurements. The mass distribution of the BreakBRD galaxies show no main deviation providing evidence that the mass distribution does not play a pivotal role in the recent central star formation and older disk age distribution.

# Data

## Data Sources

### Integral Field Unit Spectrocopy

- Mapping Nearby Galaxies at APO (MaNGA)[Description] - https://www.sdss4.org/surveys/manga/
  - https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/

### Value Added Catalog

- Pipe3D [Description] - https://data.sdss.org/datamodel/files/MANGA_PIPE3D/MANGADRP_VER/PIPE3D_VER/PLATE/manga.Pipe3D.cube.html#hdu1

  - https://data.sdss.org/sas/dr17/manga/spectro/pipe3d/v3_1_1/3.1.1/

<!-- ## Data Acquisition -->

## Data Preprocessing
1. **Sample Selection**: Galaxies were chosen from the SDSS-IV MaNGA survey, focusing on centrally star-forming galaxies with photometrically red disks (BreakBRD), using Dn4000 absorption index and g-r color cuts to identify relevant samples.

2. **Cross-Matching with MaNGA**: The selected galaxies were matched to MaNGA IFU spectroscopic observations, ensuring adequate radial coverage and spatial resolution, with observations processed through MaNGA's DRP and Pipe3D VAC pipelines for stellar and emission line data.

3. **AGN and Merger Removal**: Galaxies with central AGN ionization or significant structural disturbances from mergers were excluded using BPT diagrams and visual inspections, respectively, to ensure emission was dominated by star formation.

4. **Radial Profile Construction**: Radial profiles for each galaxy were created using elliptical coordinates and effective radii, binning spaxel data from the center to outer disk and plotting median values to analyze star formation and stellar population gradients.

5. **Stellar Mass and Age Maps**: Data products from Pipe3D were used to analyze stellar mass surface density and luminosity-weighted stellar ages, providing insights into the spatial distribution of stellar populations.

6. **Data Cleaning and Filtering**: Further quality checks included removing galaxies with low signal-to-noise spaxels, ensuring reliable data across radial profiles for subsequent analysis.

<!-- # Code Structure -->

# Results and Evaluation
Here's a continuation summarizing the results from your paper:

1. **Stellar Age Radial Distribution**:
   - The BreakBRD galaxies display an increasing Dn4000 index radial profile, suggesting a transition from a younger central stellar population to an older outer disk. This pattern is in contrast to the relatively flat profiles observed in centrally star-forming (CSF), centrally green valley (CGV), and centrally quiescent (CQC) control samples.
   - The luminosity-weighted stellar age profiles reinforce this trend, with BreakBRD galaxies showing younger stellar populations in the center compared to the disk, which aligns more closely with CGV galaxies. This indicates that BreakBRD galaxies may have experienced recent central star formation while the outer disk remains older.

2. **Stellar Mass Surface Density**:
   - The BreakBRD sample shows a monotonic decrease in stellar mass surface density from the center to the outskirts, consistent with inside-out mass growth. This trend is similar across all comparison samples, suggesting that mass assembly does not significantly influence the unique central star formation observed in BreakBRD galaxies.

3. **Comparison with Control Samples**:
   - Although BreakBRD galaxies have similar central stellar ages to CSF galaxies, their outer regions are noticeably older. The CGV and CQC samples exhibit more uniform stellar age distributions, supporting typical inside-out formation. The BreakBRD galaxies' distinct radial age gradient suggests potential mechanisms suppressing star formation in the outer disk.

4. **Implications for Galaxy Evolution**:
   - The results indicate that BreakBRD galaxies deviate from the inside-out formation model, likely due to mechanisms enhancing central star formation while suppressing it in the disk. This could be caused by factors such as gas inflows or environmental effects like ram-pressure stripping, but the exact mechanism remains uncertain.

These findings support the hypothesis that BreakBRD galaxies represent a unique case in galaxy evolution, characterized by centrally concentrated recent star formation and an older, potentially suppressed outer disk.

## Visualizations
### Statistical Analysis

<div align="center">
  <img src="images/m31_analysis_map_subplot.jpeg" alt="Spatial Metallicity Map" width="600"/>
  <p><b>Figure 1:</b> Maps of M31 RGB median metallicity assuming a fiduicial age of $4$ Gyr in $0.01$" square bins. The red cross shows the center of M31. The top map shows the original M31 RGB map and the bottom shows the map after excluding high dust mass regions, removing the well known dust ring of M31</p>
</div>

