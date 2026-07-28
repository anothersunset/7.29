import unittest
from src.statistics import mean_ci95,mean_std,wilson_interval
class StatisticsTests(unittest.TestCase):
    def test_wilson_bounds(self):
        for successes,total in ((0,10),(5,10),(10,10)):
            lo,hi=wilson_interval(successes,total);self.assertTrue(0<=lo<=hi<=1)
    def test_mean_std(self):
        mean,std=mean_std((1,2,3));self.assertEqual(mean,2);self.assertAlmostEqual(std,1);self.assertEqual(mean_std((4,)),(4,0.0))
    def test_mean_ci95(self):
        mean,std,lo,hi=mean_ci95((1,2,3));self.assertEqual(mean,2);self.assertEqual(std,1);self.assertLess(lo,mean);self.assertGreater(hi,mean)
    def test_invalid(self):
        with self.assertRaises(ValueError):wilson_interval(1,0)
        with self.assertRaises(ValueError):mean_std(())
