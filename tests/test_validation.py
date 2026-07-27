import unittest
from src.validation import validate_matrix
class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.rows=((3,),(2,1),(4,),(2,2),(2,2)); self.cols=((1,2),(5,),(3,),(3,),(4,)); self.matrix=((1,1,1,0,0),(0,1,1,0,1),(0,1,1,1,1),(1,1,0,1,1),(1,1,0,1,1))
    def test_valid(self):
        r=validate_matrix(self.matrix,self.rows,self.cols); self.assertTrue(r.valid); self.assertEqual(r.row_mismatches,()); self.assertEqual(r.col_mismatches,())
    def test_change_detected(self):
        m=[list(r) for r in self.matrix]; m[0][0]=0; r=validate_matrix(m,self.rows,self.cols); self.assertFalse(r.valid); self.assertIn(1,r.row_mismatches); self.assertIn(1,r.col_mismatches)
    def test_invalid(self):
        for call in [lambda:validate_matrix(((1,0),),((1,),),((1,),)),lambda:validate_matrix(((2,),),((1,),),((1,),)),lambda:validate_matrix((),(),())]:
            with self.assertRaises(ValueError): call()
