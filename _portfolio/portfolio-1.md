---
title: "Invariant Mass Reconstruction of the Z Boson"
collection: portfolio
permalink: /portfolio/z-boson/
excerpt: "Reconstructing the Z₀ boson mass using simulated LHC collision data."
---

## Overview

This project analyses simulated proton–proton collision data to reconstruct
the invariant mass distribution of the Z₀ boson using relativistic kinematics.

## Physics Background

The invariant mass is computed using:

![How invariant mass is computed](/images/invariant_mass_calculations.png)

$$
m = \sqrt{(E_1 + E_2)^2 - |\vec{p}_1 + \vec{p}_2|^2}
$$

## Methodology

- Event selection
- Four-momentum reconstruction
- Histogramming and Breit–Wigner fitting

## Results

![Invariant mass plot](/images/IRIS_results.png)

The reconstructed peak is consistent with the accepted Z boson mass.

## Tools Used

- Python, NumPy, Pandas
- Matplotlib
- CERN-inspired data formats
