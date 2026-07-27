"""Solve and verify the four Problem 1 worksheets."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from src.excel_io import Problem1Record,load_puzzles,write_problem1_workbook
from src.solver import solve
from src.validation import validate_matrix
SHEETS=("第一问1","第一问2","第一问3","第一问4")
def run_problem1(input_path: Path,output_dir: Path)->tuple[Problem1Record,...]:
    records=[]
    for puzzle in load_puzzles(input_path,SHEETS):
        result=solve(puzzle.row_clues,puzzle.col_clues,max_solutions=2)
        if result.solution_count!=1 or not result.exhausted: raise RuntimeError(f"{puzzle.name}: expected one proven unique solution, got {result.solution_count}, exhausted={result.exhausted}")
        matrix=result.solutions[0]; report=validate_matrix(matrix,puzzle.row_clues,puzzle.col_clues)
        if not report.valid: raise RuntimeError(f"{puzzle.name}: validation failed")
        records.append(Problem1Record(puzzle,matrix,result.solution_count,result.exhausted,result.visited_nodes,report))
    output_dir.mkdir(parents=True,exist_ok=True); write_problem1_workbook(records,output_dir/"problem1_results.xlsx")
    payload={"input_file":input_path.name,"problems":[{"name":r.puzzle.name,"size":r.puzzle.size,"solution_count":r.solution_count,"exhausted":r.exhausted,"is_unique":r.is_unique,"visited_nodes":r.visited_nodes,"validation_passed":r.validation.valid,"row_mismatches":list(r.validation.row_mismatches),"col_mismatches":list(r.validation.col_mismatches),"matrix":[list(row) for row in r.matrix]} for r in records]}
    (output_dir/"problem1_summary.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8"); return tuple(records)
def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); p.add_argument("--output-dir",type=Path,default=Path("outputs/problem1")); a=p.parse_args()
    for r in run_problem1(a.input,a.output_dir): print(f"{r.puzzle.name}: size={r.puzzle.size}, solutions={r.solution_count}, unique={r.is_unique}, nodes={r.visited_nodes}, valid={r.validation.valid}")
if __name__=="__main__": main()
