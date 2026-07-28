"""Add reproducible bootstrap confidence intervals to Problem 3 results."""
from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path
from src.statistics import bootstrap_mean_ci

def run(input_csv:Path,output_dir:Path,resamples:int=5000,seed:int=20260728):
    groups=defaultdict(list)
    with input_csv.open(encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):groups[float(row["target_rho"])].append(row)
    output_dir.mkdir(parents=True,exist_ok=True);summaries=[]
    for index,rho in enumerate(sorted(groups)):
        rows=groups[rho];values=[float(r["uncertain_count"]) for r in rows];multi=[float(r["uncertain_count"]) for r in rows if int(r["is_unique"])==0]
        mean,low,high=bootstrap_mean_ci(values,resamples,seed+2*index)
        if multi:conditional_mean,conditional_low,conditional_high=bootstrap_mean_ci(multi,resamples,seed+2*index+1)
        else:conditional_mean=conditional_low=conditional_high=None
        status="usable" if len(multi)>=30 else ("insufficient" if multi else "undefined")
        summaries.append({"target_rho":rho,"trials":len(rows),"nonunique_count":len(multi),"mean_uncertain":mean,"bootstrap95_low":low,"bootstrap95_high":high,"conditional_multi_mean_uncertain":conditional_mean,"conditional_bootstrap95_low":conditional_low,"conditional_bootstrap95_high":conditional_high,"conditional_reliability":status})
    with (output_dir/"formal_bootstrap_summary.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=summaries[0].keys());writer.writeheader();writer.writerows(summaries)
    payload={"method":"percentile bootstrap","resamples":resamples,"confidence":.95,"seed":seed,"summaries":summaries}
    (output_dir/"formal_bootstrap_summary.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    return summaries

def main():
    parser=argparse.ArgumentParser();parser.add_argument("input",type=Path);parser.add_argument("--output-dir",type=Path,default=Path("outputs/problem3"));parser.add_argument("--resamples",type=int,default=5000);parser.add_argument("--seed",type=int,default=20260728);args=parser.parse_args()
    if args.resamples<=0:parser.error("resamples must be positive")
    run(args.input,args.output_dir,args.resamples,args.seed)
if __name__=="__main__":main()
