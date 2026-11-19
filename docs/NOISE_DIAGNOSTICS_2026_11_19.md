# Noise diagnostics (19 November 2026)

Three standalone, synthetic-data analyses: (1) non-overlapping Allan deviation versus averaging time, (2) inverse-variance weighted template amplitude with an optional fitted constant baseline, and (3) finite-ensemble boxcar smoothing bias/variance/MSE, excluding convolution edges.

Allan deviation uses equally spaced samples, complete non-overlapping blocks, and requires at least three block means; it is not an uncertainty estimate for arbitrary nonstationary drift. The template fit assumes independent known Gaussian errors and a fixed template; reported errors are formal and do not include template uncertainty. The smoothing experiment uses population variance across supplied realizations and is not an observational instrument characterization.

Run: `python -m unittest discover -s tests -p "test_*.py"` (requires numpy). Eight combined cross-repository local development tests passed before publication; the exact published branch heads and full remote CI remain to be checked. The smoothing topic has related prior PR work: review overlap before merging.

Code and tests were prepared with AI assistance for scientific review. No new observations or discoveries are claimed.
