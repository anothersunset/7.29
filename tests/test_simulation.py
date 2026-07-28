import random,unittest
from src.csp_solver import solve_csp
from src.simulation import clues,evaluate,generate_matrix
class SimulationTests(unittest.TestCase):
    def test_fixed_density_and_reproducibility(self):
        a=generate_matrix(5,.4,random.Random(7));b=generate_matrix(5,.4,random.Random(7));c=generate_matrix(5,.4,random.Random(8));self.assertEqual(a,b);self.assertNotEqual(a,c);self.assertEqual(sum(map(sum,a)),10)
    def test_fixed_cells(self):
        rows,cols=clues(((1,0),(0,1)));self.assertEqual(solve_csp(rows,cols,max_solutions=1,fixed_cells={(0,0):1}).solution_count,1);self.assertEqual(solve_csp(rows,cols,max_solutions=1,fixed_cells={(0,0):0}).solution_count,1)
    def test_evaluate_known_cases(self):
        self.assertEqual(evaluate(((1,),)),(True,0));unique,uncertain=evaluate(((1,0),(0,1)));self.assertFalse(unique);self.assertEqual(uncertain,4)
    def test_bad_parameters(self):
        with self.assertRaises(ValueError):generate_matrix(0,.5,random.Random())
        with self.assertRaises(ValueError):generate_matrix(5,1.1,random.Random())
