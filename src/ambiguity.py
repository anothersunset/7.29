"""Exact ambiguous-cell analysis with one propagated CSP root."""
from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from .encoding import encode_line,parse_clue
from .patterns import generate_patterns
from .solver import Matrix
@dataclass(frozen=True,slots=True)
class AmbiguityResult:
    ambiguous_cells:tuple[tuple[int,int],...];search_exhausted:bool;visited_nodes:int;propagation_rounds:int;removed_patterns:int;locally_fixed_count:int
    @property
    def uncertain_count(self)->int:return len(self.ambiguous_cells)
def analyze_ambiguity_csp(row_clues:Sequence[Sequence[int]],col_clues:Sequence[Sequence[int]],reference:Matrix)->AmbiguityResult:
    if not row_clues or len(row_clues)!=len(col_clues):raise ValueError("clues must define a non-empty square")
    rows=tuple(parse_clue(c) for c in row_clues);cols=tuple(parse_clue(c) for c in col_clues);n=len(rows)
    if len(reference)!=n or any(len(r)!=n for r in reference) or any(v not in (0,1) for r in reference for v in r):raise ValueError("invalid reference matrix")
    if tuple(encode_line(r) for r in reference)!=rows or tuple(encode_line(tuple(reference[i][j] for i in range(n))) for j in range(n))!=cols:raise ValueError("reference does not satisfy clues")
    root_rows=[list(generate_patterns(n,c)) for c in rows];root_cols=[list(generate_patterns(n,c)) for c in cols];nodes=0;rounds=0;removed=0
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
    if not propagate(root_rows,root_cols):raise RuntimeError("reference puzzle unexpectedly inconsistent")
    unresolved={(i,j) for i in range(n) for j in range(n) if len({p[j] for p in root_rows[i]})>1 and len({p[i] for p in root_cols[j]})>1};locally_fixed=n*n-len(unresolved);ambiguous=set();proven_fixed=set()
    def find_one(target):
        nonlocal nodes
        ti,tj=target;opposite=1-reference[ti][tj];rd=[d.copy() for d in root_rows];cd=[d.copy() for d in root_cols];rd[ti]=[p for p in rd[ti] if p[tj]==opposite];cd[tj]=[p for p in cd[tj] if p[ti]==opposite]
        def dfs(rdom,cdom):
            nonlocal nodes
            nodes+=1
            if not propagate(rdom,cdom):return None
            choices=[(len(d),"r",i) for i,d in enumerate(rdom) if len(d)>1]+[(len(d),"c",j) for j,d in enumerate(cdom) if len(d)>1]
            if not choices:return tuple(d[0] for d in rdom)
            _,kind,index=min(choices);domain=rdom[index] if kind=="r" else cdom[index]
            for pattern in domain:
                nr=[d.copy() for d in rdom];nc=[d.copy() for d in cdom]
                if kind=="r":nr[index]=[pattern]
                else:nc[index]=[pattern]
                found=dfs(nr,nc)
                if found is not None:return found
            return None
        return dfs(rd,cd)
    while unresolved-ambiguous-proven_fixed:
        target=min(unresolved-ambiguous-proven_fixed);witness=find_one(target)
        if witness is None:proven_fixed.add(target)
        else:ambiguous.update((i,j) for i,j in unresolved if witness[i][j]!=reference[i][j])
    return AmbiguityResult(tuple((i+1,j+1) for i,j in sorted(ambiguous)),True,nodes,rounds,removed,locally_fixed)
