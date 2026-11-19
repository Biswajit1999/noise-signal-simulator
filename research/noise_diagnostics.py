"""Classical diagnostics for uniformly sampled noisy signals (synthetic examples)."""
import numpy as np


def _vectors(time, values):
    t = np.asarray(time, dtype=float)
    y = np.asarray(values, dtype=float)
    if t.ndim != 1 or y.shape != t.shape or t.size < 4 or not np.all(np.isfinite(t)) or not np.all(np.isfinite(y)) or not np.all(np.diff(t) > 0):
        raise ValueError('time and values must be finite aligned vectors with increasing time')
    return t, y


def allan_deviation(time, values, averaging_samples):
    """Non-overlapping Allan deviation of consecutive block means; no detrending."""
    t, y = _vectors(time, values)
    dt = np.diff(t)
    if not np.allclose(dt, dt[0], rtol=1e-6, atol=0):
        raise ValueError('uniform sampling required')
    m = int(averaging_samples)
    if m != averaging_samples or m < 1 or len(y) // m < 3:
        raise ValueError('need at least three complete blocks')
    means = y[:(len(y)//m)*m].reshape(-1, m).mean(axis=1)
    return float(m * dt[0]), float(np.sqrt(0.5 * np.mean(np.diff(means)**2)))


def weighted_template_amplitude(observed, template, sigma, include_offset=True):
    """Weighted least squares template amplitude, optionally profiling a constant offset."""
    y = np.asarray(observed, float)
    x = np.asarray(template, float)
    s = np.asarray(sigma, float)
    if y.ndim != 1 or y.size < 3 or x.shape != y.shape or s.shape != y.shape or not np.all(np.isfinite(y)) or not np.all(np.isfinite(x)) or not np.all(np.isfinite(s)) or np.any(s <= 0):
        raise ValueError('invalid vectors or uncertainties')
    a = np.column_stack((x, np.ones_like(x))) if include_offset else x[:, None]
    aw = a / s[:, None]
    yw = y / s
    if np.linalg.matrix_rank(aw) != aw.shape[1]:
        raise ValueError('degenerate template and offset')
    coefficients = np.linalg.lstsq(aw, yw, rcond=None)[0]
    covariance = np.linalg.inv(aw.T @ aw)
    return float(coefficients[0]), float(np.sqrt(covariance[0, 0]))


def smoothing_bias_variance(truth, realizations, window):
    """Empirical bias/variance/MSE for centered boxcar smoothing, excluding edge samples."""
    target = np.asarray(truth, float)
    draws = np.asarray(realizations, float)
    k = int(window)
    if target.ndim != 1 or draws.ndim != 2 or draws.shape[1] != target.size or draws.shape[0] < 2 or k != window or k < 1 or k % 2 != 1 or k > target.size or not np.all(np.isfinite(draws)) or not np.all(np.isfinite(target)):
        raise ValueError('invalid realizations or odd window')
    smooth = np.array([np.convolve(r, np.ones(k)/k, mode='valid') for r in draws])
    ref = target[k//2:target.size-k//2]
    bias = smooth.mean(axis=0) - ref
    variance = smooth.var(axis=0, ddof=0)
    return {'bias_squared': float(np.mean(bias**2)), 'variance': float(np.mean(variance)), 'mse': float(np.mean((smooth-ref)**2))}
