import unittest
from sensitivity import familywise_fap, threshold_for_fap, matched_overlap, ar1_mean_variance

class NoiseTests(unittest.TestCase):
    def test_single_trial(self): self.assertAlmostEqual(familywise_fap(0,1),.5)
    def test_two_trials(self): self.assertAlmostEqual(familywise_fap(0,2),.75)
    def test_inverse(self): self.assertAlmostEqual(familywise_fap(threshold_for_fap(.01,100),100),.01)
    def test_orthogonal(self): self.assertAlmostEqual(matched_overlap([1,0],[0,1]),0)
    def test_aligned(self): self.assertAlmostEqual(matched_overlap([1,2],[2,4]),1)
    def test_white(self): self.assertAlmostEqual(ar1_mean_variance(20,0,2),.2)
    def test_positive_correlation(self): self.assertGreater(ar1_mean_variance(20,.5),ar1_mean_variance(20,0))
if __name__=="__main__": unittest.main()
