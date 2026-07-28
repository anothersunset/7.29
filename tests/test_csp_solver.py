import random,unittest
from src.encoding import encode_line
from src.solver import solve
from src.csp_solver import solve_csp
class CspTests(unittest.TestCase):
    def compare(self,rows,cols):
        a=solve(rows,cols);b=solve_csp(rows,cols);self.assertTrue(a.exhausted);self.assertTrue(b.exhausted);self.assertEqual(set(a.solutions),set(b.solutions))
    def test_fixed_cases(self):
        self.compare(((0,),),((0,),));self.compare(((1,),),((1,),));self.compare(((1,),(1,)),((1,),(1,)));self.compare(((2,),(2,)),((1,),(1,)));self.compare(((3,),(2,1),(4,),(2,2),(2,2)),((1,2),(5,),(3,),(3,),(4,)))
    def test_limits(self):
        r=solve_csp(((1,),(1,)),((1,),(1,)),max_solutions=1);self.assertEqual(r.solution_count,1);self.assertFalse(r.exhausted)
    def test_random_small(self):
        rng=random.Random(20260727)
        for _ in range(12):
            n=4;m=tuple(tuple(rng.randrange(2) for _ in range(n)) for _ in range(n));rows=tuple(encode_line(r) for r in m);cols=tuple(encode_line(tuple(m[i][j] for i in range(n))) for j in range(n));self.compare(rows,cols)
