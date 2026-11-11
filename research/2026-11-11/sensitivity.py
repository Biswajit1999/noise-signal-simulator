"""Independent Gaussian-search and correlated-noise sensitivity calculations.

Conditional mathematical checks; not a calibrated detection pipeline.
"""
import math
from statistics import NormalDist

_NORMAL = NormalDist()

def familywise_fap(threshold, trials):
    """One-sided P(max Z_i > threshold), independent standard-normal trials."""
    if not math.isfinite(threshold) or not isinstance(trials, int) or trials < 1:
        raise ValueError("invalid search parameters")
    q = _NORMAL.cdf(-threshold)
    return -math.expm1(trials * math.log1p(-q))

def threshold_for_fap(fap, trials):
    if not 0 < fap < 1 or not isinstance(trials, int) or trials < 1:
        raise ValueError("invalid false-alarm probability")
    q = -math.expm1(math.log1p(-fap) / trials)
    return -_NORMAL.inv_cdf(q)

def matched_overlap(template, signal):
    """Expected relative matched-filter SNR, white Gaussian noise."""
    if not template or len(template) != len(signal):
        raise ValueError("mismatched or empty vectors")
    if any(not math.isfinite(x) for x in list(template) + list(signal)):
        raise ValueError("nonfinite samples")
    aa = sum(x*x for x in template)
    bb = sum(x*x for x in signal)
    if aa <= 0 or bb <= 0:
        raise ValueError("zero norm")
    return sum(x*y for x,y in zip(template,signal)) / math.sqrt(aa*bb)

def ar1_mean_variance(n, rho, sigma=1):
    """Variance of sample mean with stationary AR(1) covariance."""
    if not isinstance(n,int) or n < 1 or not -1 < rho < 1 or not math.isfinite(sigma) or sigma <= 0:
        raise ValueError("invalid AR(1) parameters")
    return sigma**2 * (n + 2*sum((n-k)*rho**k for k in range(1,n))) / n**2
