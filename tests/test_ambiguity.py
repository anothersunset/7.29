import unittest
from src.ambiguity import analyze_ambiguity_csp
from src.simulation import clues
class AmbiguityTests(unittest.TestCase):
    def test_unique(self):
        m=((1,),);rows,cols=clues(m);r=analyze_ambiguity_csp(rows,cols,m);self.assertEqual(r.uncertain_count,0);self.assertTrue(r.search_exhausted)
    def test_two_solutions(self):
        m=((1,0),(0,1));rows,cols=clues(m);r=analyze_ambiguity_csp(rows,cols,m);self.assertEqual(r.ambiguous_cells,((1,1),(1,2),(2,1),(2,2)))
    def test_invalid_reference(self):
        with self.assertRaises(ValueError):analyze_ambiguity_csp(((1,),(1,)),((1,),(1,)),((1,1),(0,0)))
