# Research Quality Upgrade

This repository has been upgraded with a compact research-quality layer: reference anchors, validation checks, and explicit scientific/software boundaries.

## Scope

Scientific signal-to-noise simulator for detector noise, smoothing, weak-signal recovery and measurement uncertainty.

## Equations And Models

- SNR = signal / noise
- Poisson noise sigma = sqrt(N)
- Weighted mean inverse-variance estimator

## Reference Anchors

The file `data/research-reference.json` stores benchmark anchors used by `scripts/validate_repository.mjs`. These are intentionally small and auditable so the repository can be checked without network access.

## Reproducibility Upgrade

The validation layer checks source files, reference data, README citations, and incomplete scaffold markers.

## References

- Bevington, P.R. and Robinson, D.K., 2003. Data Reduction and Error Analysis for the Physical Sciences. McGraw-Hill.
