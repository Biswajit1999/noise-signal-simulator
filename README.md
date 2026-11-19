<p align="center">
  <img src="images/hero.png" alt="Noise + Signal Simulator" width="900">
</p>

# Noise + Signal Simulator

> Interactive scientific tool for exploring how noise affects weak signals and how smoothing can help recover hidden patterns.

![Python](https://img.shields.io/badge/Python-Scientific-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-Interactive-yellow)
![Physics](https://img.shields.io/badge/Physics-Signal_Processing-purple)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## What this project does

This project simulates a clean scientific signal, adds random noise, and then applies smoothing to show how hidden patterns can be recovered.

Users can explore:

- true signal
- noisy observation
- smoothed recovery
- noise level
- smoothing window
- signal-to-noise ratio

---

## Why this matters

Noise is unavoidable in real scientific measurements.

In astronomy and instrumentation, weak signals are often affected by:

- detector noise
- photon noise
- sky background
- thermal effects
- electronic noise
- environmental fluctuations

Understanding signal-to-noise ratio is essential for interpreting data from telescopes, spectrographs, detectors, and laboratory instruments.

---

## Visual Understanding

### When longer averaging stops helping

![Allan deviation falls for simulated white noise and rises at long averaging times when linear drift is added](web/allan-stability.svg)

Both curves use the same seeded synthetic white noise. One adds a linear drift of 0.002 units per second. The curves compare non-overlapping Allan deviation at the same averaging times. [Open the simulator](https://biswajit1999.github.io/noise-signal-simulator/web/) or regenerate the plot with `python -m scripts.plot_allan_stability` after installing the dependencies in `requirements.txt`.

### Noisy Scientific Signal

<p align="center">
  <img src="images/noisy_signal.png" width="800">
</p>

A weak signal can be hidden beneath random fluctuations.

---

### Signal Recovery

<p align="center">
  <img src="images/signal_recovery.png" width="800">
</p>

Smoothing can help reveal the underlying pattern, but excessive smoothing may remove real features.

---

### Detector Noise Context

<p align="center">
  <img src="images/detector_noise.png" width="800">
</p>

Instruments often record both real signal and unwanted noise.

---

## Physics and data-analysis background

A simplified signal-to-noise ratio can be written as:

```text
SNR = signal strength / noise strength
```

In this project:

signal strength is estimated from the spread of the true signal
noise strength is estimated from the spread of the random noise

This is a simplified educational model. See the [numerical diagnostics and their assumptions](docs/NOISE_DIAGNOSTICS_2026_11_19.md) for stability, template-amplitude fitting and smoothing bias.
