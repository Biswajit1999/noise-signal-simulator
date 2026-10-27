"""Independent numerical and physics checks for the AR(1) noise model."""
import unittest
import numpy as np
from research.noise_robustness import ar1_noise, precision_dot, fit_template, smoothing_risk


class NoiseResearchTests(unittest.TestCase):
    def test_stationary_ar1_variance_and_lag(self):
        x = ar1_noise(40000, 2.0, 0.65, np.random.default_rng(8))
        self.assertAlmostEqual(np.std(x), 2.0, delta=0.07)
        self.assertAlmostEqual(np.corrcoef(x[:-1], x[1:])[0, 1], 0.65, delta=0.025)

    def test_precision_matches_dense_inverse(self):
        n, rho, sigma = 9, -0.35, 1.7
        c = sigma**2 * rho**np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
        v = np.arange(n, dtype=float) - 3
        self.assertTrue(np.allclose(precision_dot(v, sigma, rho), np.linalg.solve(c, v), rtol=1e-12))
        self.assertTrue(np.allclose(precision_dot(np.column_stack((v, v**2)), sigma, rho)[:, 0], np.linalg.solve(c, v)))

    def test_single_observation_precision(self):
        self.assertAlmostEqual(precision_dot(np.array([4.]), 2., 0.7)[0], 1.)

    def test_gls_noiseless_amplitude_and_baseline(self):
        t = np.sin(np.linspace(0, 8, 100))
        result = fit_template(2.3*t - 0.4, t, 0.2, 0.7)
        self.assertAlmostEqual(result['amplitude'], 2.3, places=11)
        self.assertAlmostEqual(result['offset'], -0.4, places=11)
        self.assertAlmostEqual(result['chi2_reduced'], 0., places=10)

    def test_gls_uncertainty_calibration(self):
        rng = np.random.default_rng(4)
        t = np.sin(np.linspace(0, 12, 80))
        fits = [fit_template(1.5*t + ar1_noise(80, .5, .6, rng), t, .5, .6) for _ in range(300)]
        spread = np.std([f['amplitude'] for f in fits], ddof=1)
        self.assertAlmostEqual(spread / fits[0]['sigma_amplitude'], 1., delta=.16)

    def test_degenerate_template_rejected(self):
        with self.assertRaises(ValueError):
            fit_template(np.ones(10), np.ones(10), 1., 0.)

    def test_smoothing_risk_bias_variance_identity(self):
        x = np.sin(np.linspace(0, 8*np.pi, 200))
        result = smoothing_risk(x, .3, .5, (1, 5, 15), trials=100, seed=2)
        for r in result:
            self.assertAlmostEqual(r['mse'], r['bias_squared']+r['variance'], places=12)
        self.assertLess(result[1]['variance'], result[0]['variance'])

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            ar1_noise(5, 1., 1., np.random.default_rng(1))
        with self.assertRaises(ValueError):
            smoothing_risk(np.ones(5), .2, 0., (7,))


if __name__ == '__main__':
    unittest.main()
