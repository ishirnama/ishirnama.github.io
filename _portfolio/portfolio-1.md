---
title: "Invariant Mass Reconstruction of the Z Boson"
collection: portfolio
permalink: /portfolio/portfolio-1/
excerpt: "Reconstructing the Z₀ boson mass using simulated LHC collision data."
---

## Big Data ATLAS Challenge : Finding The Invariant Mass of The Z Boson

![Scientific Research Poster : Finding The Invariant Mass of The Z boson](/images/IRIS_poster.png)

This scientific research poster is about the process of calculating the invariant mass of the Z boson.
The invariant mass is defined as the intrinsic mass of the particle while it is in motion.

This project uses data which the LHC (Lage Hadron Collider) generates by annihilating many quark and anti-quark pairs together at high energies.
After these collisions, we can observe certain patterns. For example, Z bosons typically have two main decay routes.
Z bosons can decay into either two of four leptons (a lepton is an elementary particle of half-integer spin).

![Two main decay routes of the Z boson](/images/feynman_diagrams.png)

After each collision, the annihilations which have two or four leptons as decay products are recorded.
Using the Energy-Momentum Relation : $E^2 = p^2c^2 + m_0^2c^2$ we can calculate the total energy of the collisions.
Finally, we can compute the Z boson's invariant mass using the formula below.

$$
m = \frac{1}{c^2}\sqrt{E^2 - p^2c^2}
$$

## Results

![Invariant mass plot](/images/histograms.png)

As shown in the histogram above, the invariant mass of the Z boson is consistent with it's theoretical prediction.
The In both Histograms, the peak is somewhere around 90 GeV which is very close to the theoretical prediction of 91.2 GeV.

## Tools Used

- Python, NumPy, SciPy, Pandas
- Matplotlib
- CERN-inspired data formats
