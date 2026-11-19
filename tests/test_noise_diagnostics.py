import unittest
import numpy as np
from research.noise_diagnostics import allan_deviation, weighted_template_amplitude, smoothing_bias_variance


class NoiseDiagnosticsTests(unittest.TestCase):
    def test_allan_constant(self):
        self.assertEqual(allan_deviation(np.arange(12.), np.ones(12), 2), (2., 0.))

    def test_allan_ramp(self):
        self.assertAlmostEqual(allan_deviation(np.arange(12.), np.arange(12.), 2)[1], 2/np.sqrt(2))

    def test_template(self):
        x = np.arange(8.)
        amp, err = weighted_template_amplitude(3*x+5, x, np.ones(8))
        self.assertAlmostEqual(amp, 3)
        self.assertGreater(err, 0)

    def test_smoothing(self):
        x = np.ones(15)
        self.assertAlmostEqual(smoothing_bias_variance(x, np.stack([x, x]), 3)['mse'], 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            allan_deviation([0, 1, 3, 4], [1, 2, 3, 4], 1)
        with self.assertRaises(ValueError):
            weighted_template_amplitude([1, 2, 3], [1, 1, 1], [1, 1, 1])
