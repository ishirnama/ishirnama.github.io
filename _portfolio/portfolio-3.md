---
title: "N-Body Solar System Simulation"
excerpt: "OOP simulation of planetary motion using three numerical integration methods — benchmarked for orbital accuracy and energy conservation."
collection: portfolio
---

<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;700;800&display=swap');

  .pons-page {
    font-family: 'Syne', sans-serif;
    color: #0d0d0d;
    max-width: 860px;
    margin: 0 auto;
  }

  .pons-hero {
    background: #020c1a;
    border-radius: 12px;
    padding: 48px 40px 40px;
    margin-bottom: 48px;
    position: relative;
    overflow: hidden;
  }

  .pons-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse at 20% 50%, rgba(0, 120, 255, 0.15) 0%, transparent 60%),
      radial-gradient(ellipse at 80% 20%, rgba(255, 160, 40, 0.12) 0%, transparent 50%),
      radial-gradient(ellipse at 60% 80%, rgba(100, 220, 255, 0.08) 0%, transparent 50%);
    pointer-events: none;
  }

  .pons-hero-tag {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4a9eff;
    margin-bottom: 16px;
  }

  .pons-hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    margin: 0 0 16px;
    position: relative;
  }

  .pons-hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #7a9abf;
    line-height: 1.7;
    max-width: 560px;
    position: relative;
  }

  .pons-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 28px;
    position: relative;
  }

  .pons-pill {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    padding: 5px 12px;
    border-radius: 4px;
    background: rgba(74, 158, 255, 0.12);
    color: #4a9eff;
    border: 1px solid rgba(74, 158, 255, 0.25);
    letter-spacing: 0.05em;
  }

  .pons-pill.orange {
    background: rgba(255, 160, 40, 0.1);
    color: #ffa028;
    border-color: rgba(255, 160, 40, 0.25);
  }

  .pons-pill.teal {
    background: rgba(60, 210, 180, 0.1);
    color: #3cd2b4;
    border-color: rgba(60, 210, 180, 0.25);
  }

  .pons-github-btn {
    display: inline-block;
    margin-top: 28px;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    padding: 10px 20px;
    background: #4a9eff;
    color: #000 !important;
    border-radius: 6px;
    text-decoration: none !important;
    font-weight: 700;
    letter-spacing: 0.04em;
    position: relative;
    transition: background 0.2s;
  }

  .pons-github-btn:hover {
    background: #7bbfff;
  }

  /* Stat cards */
  .pons-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 48px;
  }

  .pons-stat {
    background: #f4f7fb;
    border-radius: 10px;
    padding: 24px 20px;
    border-left: 3px solid #4a9eff;
  }

  .pons-stat.orange { border-left-color: #ffa028; }
  .pons-stat.teal   { border-left-color: #3cd2b4; }

  .pons-stat-num {
    font-size: 2rem;
    font-weight: 800;
    color: #0d0d0d;
    line-height: 1;
    margin-bottom: 6px;
  }

  .pons-stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #666;
    line-height: 1.5;
    letter-spacing: 0.04em;
  }

  /* Section headings */
  .pons-section-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a9eff;
    margin-bottom: 8px;
  }

  .pons-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 16px;
    color: #0d0d0d;
  }

  .pons-section {
    margin-bottom: 48px;
  }

  .pons-section p {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 1.85;
    color: #333;
  }

  /* Integration methods comparison */
  .pons-methods {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 24px;
  }

  .pons-method {
    border-radius: 10px;
    padding: 24px 20px;
    background: #020c1a;
    color: white;
  }

  .pons-method-name {
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 8px;
  }

  .pons-method-rms {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #7a9abf;
    margin-bottom: 12px;
  }

  .pons-method-verdict {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    line-height: 1.6;
  }

  .pons-method.winner {
    background: linear-gradient(135deg, #003875 0%, #020c1a 100%);
    border: 1px solid rgba(74, 158, 255, 0.4);
    position: relative;
  }

  .pons-method.winner::after {
    content: '★ BEST';
    position: absolute;
    top: 14px;
    right: 14px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.1em;
    color: #4a9eff;
    background: rgba(74, 158, 255, 0.15);
    padding: 3px 7px;
    border-radius: 3px;
  }

  .pons-method-rms-val {
    font-size: 1rem;
    font-weight: 700;
    color: #4a9eff;
    margin-bottom: 4px;
  }

  .pons-method.mid .pons-method-rms-val  { color: #ffa028; }
  .pons-method.bad .pons-method-rms-val  { color: #ff5a5a; }

  /* Orbit accuracy table */
  .pons-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    margin-top: 16px;
  }

  .pons-table th {
    background: #020c1a;
    color: #4a9eff;
    text-align: left;
    padding: 10px 14px;
    font-weight: 400;
    letter-spacing: 0.06em;
    font-size: 11px;
  }

  .pons-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #eee;
    color: #333;
  }

  .pons-table tr:nth-child(even) td {
    background: #f8fafc;
  }

  .pons-table .good { color: #22a06b; font-weight: 700; }

  /* Findings list */
  .pons-findings {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }

  .pons-findings li {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    line-height: 1.7;
    color: #333;
    padding: 16px 18px;
    background: #f4f7fb;
    border-radius: 8px;
    position: relative;
    padding-left: 36px;
  }

  .pons-findings li::before {
    content: '→';
    position: absolute;
    left: 14px;
    top: 16px;
    color: #4a9eff;
    font-weight: 700;
  }

  /* Alignment callout */
  .pons-callout {
    background: #020c1a;
    border-radius: 10px;
    padding: 28px 32px;
    display: flex;
    align-items: center;
    gap: 28px;
    margin-top: 24px;
  }

  .pons-callout-icon {
    font-size: 2.5rem;
    flex-shrink: 0;
  }

  .pons-callout-text {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: #7a9abf;
    line-height: 1.7;
  }

  .pons-callout-text strong {
    color: #fff;
    font-weight: 700;
  }

  @media (max-width: 640px) {
    .pons-stats, .pons-methods, .pons-findings { grid-template-columns: 1fr; }
    .pons-hero h1 { font-size: 1.8rem; }
  }
</style>

<div class="pons-page">

  <div class="pons-hero">
    <div class="pons-hero-tag">Computational Physics · Numerical Methods · Python</div>
    <h1>N-Body Solar System Simulation</h1>
    <p class="pons-hero-sub">
      An OOP simulation of planetary motion across the inner Solar System, implementing and benchmarking three numerical integration methods against NASA reference data.
    </p>
    <div class="pons-pills">
      <span class="pons-pill">Python</span>
      <span class="pons-pill">NumPy</span>
      <span class="pons-pill">Matplotlib</span>
      <span class="pons-pill orange">Beeman Integration</span>
      <span class="pons-pill orange">Euler-Cromer</span>
      <span class="pons-pill orange">Direct Euler</span>
      <span class="pons-pill teal">OOP Design</span>
      <span class="pons-pill teal">Energy Conservation</span>
    </div>
    <a class="pons-github-btn" href="https://github.com/ishirnama/PONS" target="_blank">↗ View on GitHub</a>
  </div>

  <!-- Key numbers -->
  <div class="pons-stats">
    <div class="pons-stat">
      <div class="pons-stat-num">&lt;0.35%</div>
      <div class="pons-stat-label">max orbital period error vs NASA data, across all timesteps</div>
    </div>
    <div class="pons-stat orange">
      <div class="pons-stat-num">10<sup style="font-size:1rem">13</sup>×</div>
      <div class="pons-stat-label">Beeman's energy conservation advantage over Direct Euler</div>
    </div>
    <div class="pons-stat teal">
      <div class="pons-stat-num">~145 yr</div>
      <div class="pons-stat-label">first detected 6-planet alignment within φ = 10°</div>
    </div>
  </div>

  <!-- Overview -->
  <div class="pons-section">
    <div class="pons-section-label">Overview</div>
    <h2>Simulating Gravity at Scale</h2>
    <p>
      The N-body problem — predicting how multiple bodies move under mutual gravitational attraction — has no closed-form solution for three or more bodies. The system is chaotic: tiny differences in initial conditions compound into vastly different trajectories over time. This project tackled that problem by building a full simulation of six bodies (Sun, Mercury, Venus, Earth, Mars, Jupiter) from Newton's law of universal gravitation upward, implemented in Python using an object-oriented design.
    </p>
    <p style="margin-top:14px;">
      Rather than relying on a single integration method, three algorithms were implemented, tested, and compared head-to-head: <strong>Beeman, Euler-Cromer, and Direct Euler</strong>. The simulation was validated against NASA's published orbital periods and probed for energy conservation over 25 simulated years.
    </p>
  </div>

  <!-- Integration methods -->
  <div class="pons-section">
    <div class="pons-section-label">Core Results</div>
    <h2>Integration Method Comparison</h2>
    <p>All three methods were run at dt = 0.001 yr over 25 simulated years. The differences in energy conservation were dramatic.</p>
    <div class="pons-methods">
      <div class="pons-method winner">
        <div class="pons-method-name">Beeman</div>
        <div class="pons-method-rms-val">δE<sub>RMS</sub> ≈ 0.40 × 10⁻⁶</div>
        <div class="pons-method-rms">M⊕ AU² yr⁻²</div>
        <div class="pons-method-verdict">Uses both current and previous accelerations. Symplectic — energy oscillates around the true value rather than drifting. Most physically faithful over long timescales.</div>
      </div>
      <div class="pons-method mid">
        <div class="pons-method-name">Euler-Cromer</div>
        <div class="pons-method-rms-val">δE<sub>RMS</sub> ≈ 1228 × 10⁻⁶</div>
        <div class="pons-method-rms">M⊕ AU² yr⁻²</div>
        <div class="pons-method-verdict">Updates velocity before using it to advance position. Prevents long-term drift but still shows large oscillations — roughly 3,000× worse than Beeman.</div>
      </div>
      <div class="pons-method bad">
        <div class="pons-method-name">Direct Euler</div>
        <div class="pons-method-rms-val">δE<sub>RMS</sub> ≈ 1.04 × 10⁷</div>
        <div class="pons-method-rms">M⊕ AU² yr⁻²</div>
        <div class="pons-method-verdict">Energy increases monotonically throughout the simulation, never settling. Roughly 10¹³× worse than Beeman — physically unrealistic for long runs.</div>
      </div>
    </div>
  </div>

  <!-- Orbital accuracy -->
  <div class="pons-section">
    <div class="pons-section-label">Experiment 1</div>
    <h2>Orbital Period Accuracy</h2>
    <p>Simulated orbital periods were benchmarked against NASA's reference values across four timesteps using Beeman integration over 25 years.</p>
    <table class="pons-table">
      <thead>
        <tr>
          <th>Planet</th>
          <th>NASA Period (yr)</th>
          <th>Simulated (yr)</th>
          <th>Error</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Mercury</td><td>0.241</td><td>0.241</td><td class="good">0.04–0.06%</td></tr>
        <tr><td>Venus</td><td>0.615</td><td>0.614–0.615</td><td class="good">0.03–0.19%</td></tr>
        <tr><td>Earth</td><td>1.000</td><td>1.000</td><td class="good">0.00–0.03%</td></tr>
        <tr><td>Mars</td><td>1.881</td><td>1.881</td><td class="good">0.01%</td></tr>
        <tr><td>Jupiter</td><td>11.862</td><td>11.823</td><td>0.33%</td></tr>
      </tbody>
    </table>
    <p style="margin-top:14px;">
      Jupiter's slightly higher error (0.33%) is expected: it only completes 2 orbits in 25 years (versus dozens for the inner planets), and its large mass means the fixed-Sun assumption introduces more error — in reality, Jupiter's gravity causes the Sun to wobble around the system's barycenter by a detectable margin.
    </p>
  </div>

  <!-- Timestep -->
  <div class="pons-section">
    <div class="pons-section-label">Experiment 2</div>
    <h2>Timestep and Energy Conservation</h2>
    <p>
      Running Beeman integration at progressively smaller timesteps (dt = 0.001, 0.0006, 0.0001 yr) showed a clear relationship: as dt shrinks, energy fluctuations shrink with it. At dt = 0.0001 yr, the RMS deviation approaches zero — the simulation's total energy appears effectively constant. This confirms the simulation is converged and physically reliable at small timesteps. Notably, orbital period accuracy was largely unaffected by timestep — improvements averaged just 0.02% going from dt = 0.001 to dt = 0.000125 — meaning the period results are already well-converged at the coarser step.
    </p>
  </div>

  <!-- Planetary alignment -->
  <div class="pons-section">
    <div class="pons-section-label">Experiment 4</div>
    <h2>Planetary Alignment Detection</h2>
    <p>
      A custom alignment-detection algorithm was built into the simulation. At each timestep it computes each planet's angle relative to the x-axis, finds a mean direction using unit vectors (to avoid ±π wrapping errors), and checks whether every planet falls within a critical angle φ of that mean.
    </p>
    <div class="pons-callout">
      <div class="pons-callout-icon">🪐</div>
      <div class="pons-callout-text">
        With <strong>φ = 5°</strong>, no alignment was detected even across <strong>500 simulated years</strong> — illustrating just how rare true conjunctions are. Widening to <strong>φ = 10°</strong> yielded the first alignment at <strong>t ≈ 145 years</strong>.
      </div>
    </div>
  </div>

  <!-- Key findings -->
  <div class="pons-section">
    <div class="pons-section-label">Summary</div>
    <h2>Key Findings</h2>
    <ul class="pons-findings">
      <li>Beeman integration reproduces all planetary orbital periods to within 0.35% of NASA values</li>
      <li>Beeman's RMS energy deviation is ~10¹³× smaller than Direct Euler's at the same timestep</li>
      <li>Beeman is symplectic: energy fluctuates around the true value rather than drifting away</li>
      <li>Orbital period accuracy converges at dt = 0.001 yr — finer steps yield negligible improvement</li>
      <li>Reducing timestep drives δE<sub>RMS</sub> toward zero, confirming energy is conserved at dt = 0.0001 yr</li>
      <li>Jupiter's 0.33% error traces to the fixed-Sun assumption, not integration error</li>
      <li>A 6-planet alignment within φ = 10° was detected at t ≈ 145 yr; φ = 5° yielded none in 500 yr</li>
      <li>Unit-vector mean angle avoids ±π wrapping failures near the negative x-axis</li>
    </ul>
  </div>

</div>
