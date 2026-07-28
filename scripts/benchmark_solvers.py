"""Compare baseline and CSP solvers on workbook puzzles."""
from __future__ import annotations
import argparse
from pathlib import Path
from src.csp_solver import solve_csp
from src.excel_io import load_puzzles
from src.solver import solve
SHEETS=("第一问1","第一问2","第一问3","第一问4","第二问1","第二问2","第二问3")
def main():
    p=argparse.ArgumentParser();p.add_argument("input",type=Path);a=p.parse_args();print("sheet,solutions,baseline_nodes,csp_nodes,rounds,removed,equal")
    for puzzle in load_puzzles(a.input,SHEETS):
        base=solve(puzzle.row_clues,puzzle.col_clues);csp=solve_csp(puzzle.row_clues,puzzle.col_clues);print(f"{puzzle.name},{base.solution_count},{base.visited_nodes},{csp.visited_nodes},{csp.propagation_rounds},{csp.removed_patterns},{set(base.solutions)==set(csp.solutions)}")
if __name__=="__main__":main()
