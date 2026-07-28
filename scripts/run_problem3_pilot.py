"""Run the reproducible Problem 3 fixed-density experiment."""
from __future__ import annotations
import argparse,csv,json,random,time
from pathlib import Path
from src.simulation import evaluate,generate_matrix
from src.statistics import mean_ci95,mean_std,wilson_interval
def run(n:int,ratios:list[float],trials:int,seed:int,output_dir:Path,prefix:str="pilot",pilot_only:bool=True):
    rng=random.Random(seed);records=[];summaries=[];output_dir.mkdir(parents=True,exist_ok=True)
    for rho in ratios:
        group=[]
        for trial in range(1,trials+1):
            matrix=generate_matrix(n,rho,rng);start=time.perf_counter();unique,uncertain=evaluate(matrix);elapsed=time.perf_counter()-start;row={"n":n,"target_rho":rho,"actual_rho":sum(map(sum,matrix))/(n*n),"trial":trial,"is_unique":int(unique),"uncertain_count":uncertain,"elapsed_seconds":elapsed};records.append(row);group.append(row);print(f"rho={rho:.2f} trial={trial}/{trials} unique={unique} uncertain={uncertain} seconds={elapsed:.3f}",flush=True)
        successes=sum(r["is_unique"] for r in group);lo,hi=wilson_interval(successes,trials);values=[r["uncertain_count"] for r in group];mean_u,std_u,mean_u_lo,mean_u_hi=mean_ci95(values);multi=[r["uncertain_count"] for r in group if not r["is_unique"]]
        if multi:cond_mean,cond_std,cond_lo,cond_hi=mean_ci95(multi)
        else:cond_mean=cond_std=cond_lo=cond_hi=None
        mean_t,std_t=mean_std([r["elapsed_seconds"] for r in group]);summaries.append({"n":n,"target_rho":rho,"actual_rho":group[0]["actual_rho"],"trials":trials,"unique_count":successes,"nonunique_count":trials-successes,"unique_probability":successes/trials,"wilson95_low":lo,"wilson95_high":hi,"mean_uncertain":mean_u,"std_uncertain":std_u,"mean_uncertain_ci95_low":max(0.0,mean_u_lo),"mean_uncertain_ci95_high":mean_u_hi,"conditional_multi_mean_uncertain":cond_mean,"conditional_multi_std_uncertain":cond_std,"conditional_multi_ci95_low":None if cond_lo is None else max(0.0,cond_lo),"conditional_multi_ci95_high":cond_hi,"mean_seconds":mean_t,"std_seconds":std_t,"max_seconds":max(r["elapsed_seconds"] for r in group)})
    with (output_dir/f"{prefix}_results.csv").open("w",newline="",encoding="utf-8-sig") as f:w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
    with (output_dir/f"{prefix}_summary.csv").open("w",newline="",encoding="utf-8-sig") as f:w=csv.DictWriter(f,fieldnames=summaries[0].keys());w.writeheader();w.writerows(summaries)
    (output_dir/f"{prefix}_summary.json").write_text(json.dumps({"seed":seed,"pilot_only":pilot_only,"summaries":summaries},ensure_ascii=False,indent=2),encoding="utf-8");return summaries
def main():
    p=argparse.ArgumentParser();p.add_argument("--n",type=int,default=10);p.add_argument("--ratios",type=float,nargs="+",default=[.1,.3,.5,.7,.9]);p.add_argument("--trials",type=int,default=20);p.add_argument("--seed",type=int,default=20260727);p.add_argument("--prefix",default="pilot");p.add_argument("--formal",action="store_true");p.add_argument("--output-dir",type=Path,default=Path("outputs/problem3"));a=p.parse_args()
    if a.n<=0 or a.trials<=0 or any(not 0<=r<=1 for r in a.ratios):p.error("invalid parameters")
    run(a.n,a.ratios,a.trials,a.seed,a.output_dir,a.prefix,not a.formal)
if __name__=="__main__":main()
