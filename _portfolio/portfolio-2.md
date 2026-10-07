---
title: "Plastic Pollution Severity Analysis of Scottish Beaches"
collection: portfolio
permalink: /portfolio/portfolio-2/
excerpt: "A weighted severity score and interactive maps for coastal plastic pollution across Scotland."
---

## SCOTLAND SEAS: Analysing Plastic Pollution on Scottish Beaches

Plastic pollution is one of the most visible threats to Scotland's marine environment, but "how polluted is a beach?" is surprisingly hard to answer fairly — a single discarded fishing net is environmentally very different from a single crisp packet. This project builds a **weighted severity score** that accounts for *what kind* of litter is found (and what it's made of), then maps it across the Scottish coastline.

The data comes from the **SCOTLAND SEAS** citizen-science beach-clean programme, where volunteers itemise everything they collect into roughly 130 litter categories alongside survey metadata such as date, location, tide, wind and substrate.

## The Data

- **49 survey records** across **27 beaches** in **5 sea regions** (Firth of Clyde, Firth of Lorn, Little Minch, North Channel, Upper Minch), October–November 2022.
- Each record itemises litter into **~130 categories**, each column named like `X02_plastic_RopeStringCordLrg` or `X03_polystyrene_fragmentMed`.
- Beaches surveyed **exactly twice** are averaged into a single profile, so the analysis reflects a stable per-beach signature rather than a one-off count. This leaves **22 beaches**.

## Building a Severity Score

Instead of treating every item equally, each litter item is weighted by its **environmental severity** and its **material**.

**1. Parse & classify.** Each column name encodes three things: a survey code (`X01/X02/X03`), a material (`plastic`, `polystyrene`, `rubber`…), and an object (`fragmentMed`, `RopeStringCordLrg`…). The object name is split into words and matched against keyword rules to place it into one of eight pollution categories.

**2. Assign severity & material multipliers.**

| Category | Severity |
|---|---|
| hazardous | 4.5 |
| microplastics | 4.0 |
| fishing gear | 3.5 |
| sanitary & medical | 3.0 |
| industrial | 2.5 |
| consumer packaging | 2.0 |
| personal items | 1.5 |
| other | 1.0 |

| Material | Multiplier |
|---|---|
| pollutants | 2.0 |
| medical | 1.4 |
| sanitary | 1.3 |
| polystyrene | 1.2 |
| rubber | 1.1 |
| plastic | 1.0 |
| metal | 0.8 |
| cloth | 0.7 |
| glass / paper | 0.6 |
| wood | 0.5 |

**3. Weight each item and normalise.**

$$W_i = \text{severity}(c_i) \times \text{multiplier}(m_i), \qquad W_i \leftarrow \frac{W_i}{\sum_j W_j}$$

**4. Score each beach** as the weighted sum of its recorded litter, divided by the number of beaches:

$$S = \frac{1}{N}\,W^{\top} P_\mu$$

where \(N\) is the number of beaches and \(P_\mu\) is a beach's average litter-count vector (across its two surveys).

## Visualising the Results

The first map shows the **three most common plastics** at each beach; the second shows the **severity score** as colour- and size-scaled markers (viridis colour scale, radius \(r = 25\sqrt{s/s_{\max}}\)).

<iframe src="/files/scotland_top3_plastics.html" width="100%" height="540" style="border:0; border-radius:8px;" loading="lazy" title="Top 3 plastics per Scottish beach"></iframe>

<iframe src="/files/scotland_severity_map.html" width="100%" height="540" style="border:0; border-radius:8px;" loading="lazy" title="Plastic pollution severity on Scottish beaches"></iframe>

## Key Findings

- **The Black Beach** (Isle of Mull) is by far the most polluted, scoring **0.80** — more than double the next-worst beach, Talisker Bay on Skye (**0.35**).
- **Unclassified items** ("other", ~1,438 — ropes, strings and objects outside the seven categories) and **microplastics** (~1,377) are the two largest groups, followed by **fishing gear** (~903) and **consumer packaging** (~713).
- **Hazardous** items are rare (~100) but weighted at 4.5, so a few fuel canisters, shotgun cartridges or fertiliser containers can sharply raise a beach's score.
- The worst-affected beaches are on the **west coast and Hebridean islands** (Mull, Skye, Tiree, Islay), consistent with prevailing westerly currents depositing marine litter on exposed, windward shores. By contrast, **Carskey Bay** on Kintyre scores just **0.001**.

## Tools Used

- Python, Pandas, NumPy
- Matplotlib (viridis colour scale)
- Leaflet (interactive maps)
- SCOTLAND SEAS beach-clean dataset
