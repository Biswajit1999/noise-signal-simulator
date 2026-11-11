# Gaussian search and correlated-noise audit (11 November 2026)

Independent, synthetic mathematical sensitivity module. Four functions cover three related diagnostics: (1) exact one-sided familywise false-alarm probability and inverse threshold for **independent** standard-normal trials; (2) normalized template overlap, equivalent to expected relative matched-filter SNR under white homoscedastic Gaussian noise; (3) exact finite-n arithmetic-mean variance under stationary AR(1) covariance sigma² rho^|i-j|.

Assumptions: the independent-trials formula is **not valid** when search templates are correlated; template overlap is not a detection probability; the AR(1) covariance is a model assumption, not estimated detector covariance. Negative overlap is allowed for sign-reversed templates.

Reproduce: `cd research/2026-11-11 && python -m unittest -v test_sensitivity.py`.

No observational input or published detection claim. AI-assisted code preparation; scientific review required before merge.
