"""CSP solver with domain propagation and MRV branching."""
from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Integral
from .encoding import parse_clue
from .patterns import Pattern,generate_patterns
from .solver import Clue,Matrix
@dataclass(frozen=True,slots=True)
class CspSolveResult:
    solutions:tuple[Matrix,...];exhausted:bool;visited_nodes:int;propagation_rounds:int;removed_patterns:int
    @property
    def solution_count(self)->int:return len(self.solutions)
def solve_csp(row_clues:Sequence[Sequence[int]],col_clues:Sequence[Sequence[int]],max_solutions:int|None=None)->CspSolveResult:
    if not row_clues or len(row_clues)!=len(col_clues):raise ValueError("clues must define a non-empty square")
    if max_solutions is not None and (isinstance(max_solutions,bool) or not isinstance(max_solutions,Integral) or max_solutions<=0):raise ValueError("max_solutions must be positive or None")
    rows=tuple(parse_clue(c) for c in row_clues);cols=tuple(parse_clue(c) for c in col_clues);n=len(rows)
    initial_rows=[list(generate_patterns(n,c)) for c in rows];initial_cols=[list(generate_patterns(n,c)) for c in cols]
    solutions=[];nodes=0;rounds=0;removed=0;stopped=False
    def propagate(rd,cd):
        nonlocal rounds,removed
        while True:
            rounds+=1;changed=False
            col_values=[[{p[i] for p in cd[j]} for j in range(n)] for i in range(n)]
            for i in range(n):
                before=len(rd[i]);rd[i]=[p for p in rd[i] if all(p[j] in col_values[i][j] for j in range(n))];removed+=before-len(rd[i]);changed|=before!=len(rd[i])
            if any(not d for d in rd):return False
            row_values=[[{p[j] for p in rd[i]} for j in range(n)] for i in range(n)]
            for j in range(n):
                before=len(cd[j]);cd[j]=[p for p in cd[j] if all(p[i] in row_values[i][j] for i in range(n))];removed+=before-len(cd[j]);changed|=before!=len(cd[j])
            if any(not d for d in cd):return False
            if not changed:return True
    def search(rd,cd):
        nonlocal nodes,stopped
        nodes+=1
        if not propagate(rd,cd):return
        choices=[(len(d),"r",i) for i,d in enumerate(rd) if len(d)>1]+[(len(d),"c",j) for j,d in enumerate(cd) if len(d)>1]
        if not choices:solutions.append(tuple(d[0] for d in rd));return
        _,kind,index=min(choices);domain=rd[index] if kind=="r" else cd[index]
        for pattern in domain:
            if max_solutions is not None and len(solutions)>=max_solutions:stopped=True;return
            nr=[d.copy() for d in rd];nc=[d.copy() for d in cd]
            if kind=="r":nr[index]=[pattern]
            else:nc[index]=[pattern]
            search(nr,nc)
    search(initial_rows,initial_cols)
    return CspSolveResult(tuple(solutions),not stopped,nodes,rounds,removed)
