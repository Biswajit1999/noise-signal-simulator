# Correlated-noise and recovery robustness (27 October 2026)

The repository's `main.py` illustrates a damped sinusoid with white noise and a moving average. `research/noise_robustness.py` adds **independent, synthetic** analyses without changing that educational interface.

1. Stationary AR(1) noise with marginal variance `sigma²`, correlation `rho^|i-j|` and seeded draws. This is a toy colored-noise model, not a measured detector spectrum.
2. Generalized least-squares (GLS) estimation of a known template's amplitude plus constant baseline. The tridiagonal inverse covariance avoids a dense matrix. Reported errors are *conditional* on the template and exact covariance assumptions.
3. Seeded smoothing-window Monte Carlo with common interior samples, separating squared bias and variance. This exposes loss of narrow signals from over-smoothing and avoids misleading zero-padding edges.

Reproduce: `python -m unittest discover -s tests -p 'test_*_research.py' -v` (requires NumPy). No observational data or instrument performance is inferred.
