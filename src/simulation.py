"""Reproducible fixed-density simulation helpers."""
from __future__ import annotations
import random
from .encoding import encode_line
from .ambiguity import analyze_ambiguity_csp
def generate_matrix(n:int,rho:float,rng:random.Random):
    if n<=0 or not 0<=rho<=1:raise ValueError("invalid simulation parameters")
    ones=round(rho*n*n);chosen=set(rng.sample(range(n*n),ones));return tuple(tuple(int(i*n+j in chosen) for j in range(n)) for i in range(n))
def clues(matrix):
    n=len(matrix);return tuple(encode_line(r) for r in matrix),tuple(encode_line(tuple(matrix[i][j] for i in range(n))) for j in range(n))
def evaluate(matrix):
    rows,cols=clues(matrix);result=analyze_ambiguity_csp(rows,cols,matrix);return result.uncertain_count==0,result.uncertain_count
