"""Reproducible synthetic noise and signal-recovery diagnostics.

AR(1) is a deliberately simplified stationary covariance model, not detector data.
"""
from __future__ import annotations

import numpy as np


def ar1_noise(n: int, sigma: float, rho: float, rng: np.random.Generator) -> np.ndarray:
    """Draw stationary AR(1) noise with marginal standard deviation sigma."""
    if n < 1 or sigma <= 0 or not np.isfinite(sigma) or not -1 < rho < 1:
        raise ValueError("Require n>=1, finite sigma>0 and |rho|<1")
    values = np.empty(n)
    values[0] = rng.normal(scale=sigma)
    innovations = rng.normal(scale=sigma * np.sqrt(1 - rho * rho), size=n - 1)
    for i in range(1, n):
        values[i] = rho * values[i - 1] + innovations[i - 1]
    return values


def precision_dot(vector: np.ndarray, sigma: float, rho: float) -> np.ndarray:
    """Apply inverse stationary AR(1) covariance without forming a dense matrix."""
    v = np.asarray(vector, dtype=float)
    if v.ndim not in (1, 2) or v.shape[0] < 1 or sigma <= 0 or not np.isfinite(sigma) or not -1 < rho < 1:
        raise ValueError("Invalid vector, sigma or correlation")
    if not np.all(np.isfinite(v)):
        raise ValueError("Vector must be finite")
    if v.shape[0] == 1:
        return v / sigma**2
    out = (1 + rho * rho) * v.copy()
    out[0] = v[0]
    out[-1] = v[-1]
    out[1:] -= rho * v[:-1]
    out[:-1] -= rho * v[1:]
    return out / (sigma**2 * (1 - rho * rho))


def fit_template(y: np.ndarray, template: np.ndarray, sigma: float, rho: float) -> dict:
    """GLS fit of template amplitude and constant baseline, with conditional errors."""
    y, t = np.asarray(y, float), np.asarray(template, float)
    if y.ndim != 1 or t.shape != y.shape or len(y) < 3 or not np.all(np.isfinite(y)) or not np.all(np.isfinite(t)):
        raise ValueError("Need >=3 finite matched observations and template values")
    design = np.column_stack((t, np.ones_like(t)))
    weighted = precision_dot(design, sigma, rho)
    information = design.T @ weighted
    if np.linalg.cond(information) > 1e12:
        raise ValueError("Template and offset are degenerate")
    covariance = np.linalg.inv(information)
    parameters = covariance @ (design.T @ precision_dot(y, sigma, rho))
    residual = y - design @ parameters
    chi2 = float(residual @ precision_dot(residual, sigma, rho))
    return {"amplitude": float(parameters[0]), "offset": float(parameters[1]),
            "sigma_amplitude": float(np.sqrt(covariance[0, 0])),
            "chi2_reduced": chi2 / (len(y) - 2)}


def smoothing_risk(signal: np.ndarray, sigma: float, rho: float, windows: tuple[int, ...],
                   trials: int = 200, seed: int = 27) -> list[dict]:
    """Monte Carlo interior MSE and squared bias; common edge trim across windows."""
    truth = np.asarray(signal, float)
    if truth.ndim != 1 or not np.all(np.isfinite(truth)) or trials < 2 or not windows or any(w < 1 or w % 2 != 1 for w in windows):
        raise ValueError("Need finite 1D truth, >=2 trials and positive odd windows")
    margin = max(windows) // 2
    if truth.size <= 2 * margin + 2:
        raise ValueError("Signal too short for common interior")
    rng = np.random.default_rng(seed)
    estimates = {w: [] for w in windows}
    for _ in range(trials):
        noisy = truth + ar1_noise(truth.size, sigma, rho, rng)
        for w in windows:
            estimates[w].append(np.convolve(noisy, np.ones(w) / w, mode="same")[margin:truth.size-margin])
    target = truth[margin:truth.size-margin]
    result = []
    for w in windows:
        recovered = np.asarray(estimates[w])
        bias = np.mean(recovered, axis=0) - target
        result.append({"window": w, "mse": float(np.mean((recovered - target)**2)),
                       "bias_squared": float(np.mean(bias**2)),
                       "variance": float(np.mean(np.var(recovered, axis=0, ddof=0)))})
    return result
