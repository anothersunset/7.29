import unittest
from src.analysis import analyze_solutions
class AnalysisTests(unittest.TestCase):
    def test_unique(self):
        m=((1,0),(0,1));a=analyze_solutions((m,));self.assertTrue(a.is_unique);self.assertEqual(a.consensus_matrix,m);self.assertEqual(a.uncertain_count,0)
    def test_two_solutions(self):
        a=analyze_solutions((((1,0),(0,1)),((0,1),(1,0))));self.assertFalse(a.is_unique);self.assertEqual(a.solution_count,2);self.assertEqual(a.uncertain_count,4);self.assertEqual(a.uncertain_cells,((1,1),(1,2),(2,1),(2,2)));self.assertEqual(a.consensus_matrix,((None,None),(None,None)))
    def test_empty(self):
        a=analyze_solutions(());self.assertEqual(a.solution_count,0);self.assertEqual(a.consensus_matrix,())
    def test_invalid(self):
        for s in [(((1,0),),),(((2,),),),(((1,),),((1,0),(0,1)))]:
            with self.assertRaises(ValueError):analyze_solutions(s)
