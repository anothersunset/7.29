"""Solution-space analysis for unique and ambiguous cells."""
from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from .solver import Matrix
ConsensusCell=int|None
ConsensusMatrix=tuple[tuple[ConsensusCell,...],...]
@dataclass(frozen=True,slots=True)
class SolutionAnalysis:
    solution_count:int; is_unique:bool; consensus_matrix:ConsensusMatrix; uncertain_count:int; uncertain_cells:tuple[tuple[int,int],...]
def analyze_solutions(solutions:Sequence[Matrix])->SolutionAnalysis:
    if not solutions:return SolutionAnalysis(0,False,tuple(),0,tuple())
    n=len(solutions[0])
    if n==0 or any(len(m)!=n or any(len(row)!=n for row in m) for m in solutions):raise ValueError("all solutions must be non-empty square matrices of equal size")
    if any(v not in (0,1) for m in solutions for row in m for v in row):raise ValueError("solution matrices must contain only 0 and 1")
    consensus=[];uncertain=[]
    for i in range(n):
        row=[]
        for j in range(n):
            values={m[i][j] for m in solutions}
            if len(values)==1:row.append(next(iter(values)))
            else:row.append(None);uncertain.append((i+1,j+1))
        consensus.append(tuple(row))
    return SolutionAnalysis(len(solutions),len(solutions)==1,tuple(consensus),len(uncertain),tuple(uncertain))
