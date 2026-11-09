# Trial factors and matched-template mismatch (9 November 2026)

Independent synthetic-only diagnostics; existing app and simulation are unchanged.

For N **independent** one-sided standard-normal trial scores, the probability of at least one exceeding z is `1-(1-p(z))**N`, with `p(z)=0.5*erfc(z/sqrt(2))`. The inverse routine returns the threshold for a specified global false-alarm probability. Correlated template banks have an unknown effective number of trials: substituting the number of grid points is generally unjustified.

For independent equal-variance Gaussian noise, the normalized inner product of true signal and assumed template is the expected matched-filter SNR fraction, including its sign. It does not estimate power, recovery completeness, or detection probability.

Run from repository root: `python -m unittest discover -s tests -p 'test_trial_factor_audit.py'`.

AI assistance was used for code and tests. No measured detector noise, look-elsewhere calibration or observational detection is claimed.
