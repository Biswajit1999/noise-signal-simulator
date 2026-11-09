"""Synthetic-only look-elsewhere and template-mismatch diagnostics.

Independent standard-normal samples, unit-norm deterministic templates.
Not a telescope false-alarm calibration.
"""
import math
import statistics


def independent_trials_false_alarm(threshold_sigma: float, trials: int) -> float:
    """P(max of N independent standard normal scores >= threshold)."""
    if not math.isfinite(threshold_sigma) or not isinstance(trials, int) or trials < 1:
        raise ValueError("finite threshold and positive integer trial count required")
    one_tail = 0.5 * math.erfc(threshold_sigma / math.sqrt(2))
    return -math.expm1(trials * math.log1p(-one_tail))


def threshold_for_global_false_alarm(alpha: float, trials: int) -> float:
    """Invert the exact independent-trial maximum CDF by monotone bisection."""
    if not (math.isfinite(alpha) and 0 < alpha < 1) or not isinstance(trials, int) or trials < 1:
        raise ValueError("0 < alpha < 1 and positive integer trials required")
    low, high = -12.0, 12.0
    for _ in range(100):
        mid = (low + high) / 2
        if independent_trials_false_alarm(mid, trials) > alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def normalized_overlap(signal, template) -> float:
    """Expected matched-filter SNR fraction for white noise, with sign retained."""
    if len(signal) != len(template) or len(signal) == 0:
        raise ValueError("nonempty equal-length arrays required")
    a, b = [float(x) for x in signal], [float(x) for x in template]
    if not all(map(math.isfinite, a + b)):
        raise ValueError("nonfinite input")
    norm_a, norm_b = math.sqrt(sum(x*x for x in a)), math.sqrt(sum(x*x for x in b))
    if norm_a == 0 or norm_b == 0:
        raise ValueError("zero-norm template")
    return sum(x*y for x,y in zip(a,b)) / (norm_a * norm_b)
