---
title: "N-Body Simulation of the Solar System"
collection: portfolio
permalink: /portfolio/portfolio-3/
excerpt: "Testing accuracy and energy conservation across three numerical integration methods."
---

## Introduction to Computation Coursework : N-Body Simulation of the Solar System

This project involved building an N-body simulation of a subset of the Solar System (Sun, Mercury, Venus, Earth, Mars, and Jupiter) in Python using an object-oriented design. The underlying physics is Newton's law of universal gravitation, which describes the force between any two masses.

The N-body problem is a classical challenge in physics. While the motion of two bodies can be solved analytically, systems of three or more bodies behave chaotically — tiny differences in initial conditions can lead to vastly different trajectories over time. Numerical integration is the standard approach for these systems.

The simulation was built with two classes: a `Body` class storing each planet's physical attributes (mass, position, velocity, acceleration), and an `NBodySimulation` class managing the simulation loop, orbit detection, energy tracking, and alignment detection.

## Integration Methods

Three numerical integration methods were implemented and compared:

**Direct Euler** updates position using the current velocity and velocity using the current acceleration. It is the simplest method but is known to be poor at conserving energy over long timescales.

**Euler-Cromer** is a small modification to Direct Euler — it updates velocity first, then uses the updated velocity to advance position. This change prevents energy from drifting away over time.

**Beeman's method** uses both the current and previous timestep's accelerations to update position and velocity, making it more accurate and better at conserving energy.

$$
\vec{r}(t+\delta t) = \vec{r}(t) + \vec{v}(t)\cdot\delta t + \frac{1}{6}[4\vec{a}(t) - \vec{a}(t-\delta t)]\cdot\delta t^2
$$

## Experiment 1: Orbital Period Accuracy

I ran the simulation over 25 years using Beeman integration and detected each planet's orbital period by tracking when its y-coordinate crossed from negative to positive. I then compared the results to NASA's published values.

| Planet  | NASA Period (yr) | Simulated (yr) | Error  |
|---------|-----------------|----------------|--------|
| Mercury | 0.241           | 0.241          | 0.06%  |
| Venus   | 0.615           | 0.615          | 0.03%  |
| Earth   | 1.000           | 1.000          | 0.00%  |
| Mars    | 1.881           | 1.881          | 0.01%  |
| Jupiter | 11.862          | 11.823         | 0.33%  |

All planets came in under 0.35% error. Jupiter's slightly higher error is likely because it only completes about 2 orbits in 25 years, giving fewer crossings to average over. Jupiter's large mass also means the fixed-Sun assumption introduces more error than it does for the inner planets; in reality its gravity causes the Sun to wobble around the system's barycentre.

## Experiment 2: Energy Conservation

The total mechanical energy of the system is E = T + V, where T is kinetic energy and $V$ is gravitational potential energy. To measure how well each method conserves energy, I computed the RMS energy deviation δEᵣₘₛ over 25 simulated years.

![Total energy vs time and RMS deviation for all three integration methods](/images/PONS_energy_methods.png)

The results show a dramatic difference between methods:

- **Beeman**: δEᵣₘₛ ≈ 0.40×10⁻⁶ [M⊕ AU² yr⁻²] (energy fluctuates around a stable value)
- **Euler-Cromer**: δEᵣₘₛ ≈ 1228×10⁻⁶ (roughly 3,000× worse than Beeman)
- **Direct Euler**: δEᵣₘₛ ≈ 1.40×10⁷ (energy increases monotonically throughout, about 10¹³× worse than Beeman)

Beeman's method performs so well because it is symplectic — over long periods, the total energy oscillates around the true value rather than drifting away from it.

I also tested the effect of timestep on Beeman's energy conservation, using dt = 0.001, 0.0006, and 0.0001 yr(s).

![Energy conservation for Beeman at three different timesteps](/images/PONS_energy_timestep.png)

As the timestep decreases, the energy fluctuations shrink and δEᵣₘₛ approaches zero. At dt = 0.0001 yr the total energy appears effectively constant throughout the simulation.

## Experiment 4: Planetary Alignment Detection

I implemented a method that detects when all planets fall within a critical angle (φ) of a common direction. At each timestep it computes each planet's angle relative to the x-axis, calculates a mean direction using unit vectors (to avoid wrapping errors near ±π), and checks whether every planet's angular deviation from that mean is less than φ.

$$
\delta\theta_i = |\arctan2(\sin(\theta_i - \theta_\text{mean}),\ \cos(\theta_i - \theta_\text{mean}))| < \varphi
$$

| $\varphi$ (deg) | Simulation length (yr) | First alignment |
|-----------------|------------------------|-----------------|
| 5°              | 25                     | None detected   |
| 5°              | 500                    | None detected   |
| 10°             | 25                     | None detected   |
| 10°             | 250                    | t ≈ 145.25 yr   |

A 5° alignment window produced no detections even across 500 simulated years, illustrating how rare true conjunctions are. Widening to 10° revealed the first alignment at around 145 years.

## Tools Used

- Python, NumPy, Matplotlib
- Object-oriented programming (OOP)
- JSON for loading initial planetary parameters
