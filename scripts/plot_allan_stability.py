"""Compare simulated white noise and white noise with a linear drift."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from research.noise_diagnostics import allan_deviation

ROOT = Path(__file__).resolve().parents[1]
time = np.arange(4096, dtype=float)
white = np.random.default_rng(19).normal(size=time.size)
samples_per_block = 2 ** np.arange(10)

with plt.rc_context({"svg.fonttype": "none", "svg.hashsalt": "allan-stability", "font.size": 12}):
    figure, axis = plt.subplots(figsize=(8, 4.4), layout="constrained")
    for series, marker, colour, label in (
        (white, "o", "#28495c", "White noise (σ = 1)"),
        (white + 0.002 * time, "s", "#a44527", "Same noise + linear drift (0.002 units/s)"),
    ):
        tau, deviation = np.asarray(
            [allan_deviation(time, series, int(size)) for size in samples_per_block]
        ).T
        axis.loglog(tau, deviation, marker=marker, ms=4, color=colour, label=label)
    axis.set(xlabel="Averaging time, τ (s)", ylabel="Allan deviation (arbitrary units)")
    axis.set_title("Longer averaging can expose drift", loc="left", fontweight="bold")
    axis.grid(True, which="major", alpha=0.2)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(loc="best", frameon=False, fontsize=9)
    figure.savefig(ROOT / "web/allan-stability.svg", metadata={"Date": None})
    plt.close(figure)
