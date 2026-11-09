import math
import unittest
from research.trial_factor_audit import (
    independent_trials_false_alarm, threshold_for_global_false_alarm, normalized_overlap
)


class TrialFactorTests(unittest.TestCase):
    def test_one_trial(self):
        self.assertAlmostEqual(independent_trials_false_alarm(3, 1),
                               0.5 * math.erfc(3 / math.sqrt(2)))

    def test_monotonic(self):
        self.assertGreater(independent_trials_false_alarm(3, 100),
                           independent_trials_false_alarm(3, 1))

    def test_inverse(self):
        for n in (1, 100, 10000):
            z = threshold_for_global_false_alarm(0.01, n)
            self.assertAlmostEqual(independent_trials_false_alarm(z, n), 0.01, places=11)

    def test_match(self):
        self.assertAlmostEqual(normalized_overlap([1, 2], [1, 2]), 1)

    def test_orthogonal(self):
        self.assertAlmostEqual(normalized_overlap([1, 0], [0, 1]), 0)

    def test_mismatch(self):
        self.assertAlmostEqual(normalized_overlap([1, 0], [1, 1]), 1 / math.sqrt(2))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            normalized_overlap([0, 0], [1, 1])


if __name__ == "__main__":
    unittest.main()
