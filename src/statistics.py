"""Statistical summaries for Monte Carlo reconstruction experiments."""
from __future__ import annotations
from math import floor, sqrt
from random import Random
from collections.abc import Sequence

def wilson_interval(successes:int,total:int,z:float=1.959963984540054)->tuple[float,float]:
    if total<=0 or not 0<=successes<=total: raise ValueError("invalid binomial counts")
    p=successes/total; d=1+z*z/total
    center=(p+z*z/(2*total))/d
    margin=z*sqrt(p*(1-p)/total+z*z/(4*total*total))/d
    return max(0.0,center-margin),min(1.0,center+margin)

def mean_std(values:Sequence[float])->tuple[float,float]:
    if not values: raise ValueError("values must not be empty")
    mean=sum(values)/len(values)
    if len(values)==1:return mean,0.0
    variance=sum((x-mean)**2 for x in values)/(len(values)-1)
    return mean,sqrt(variance)

def mean_ci95(values:Sequence[float],z:float=1.959963984540054)->tuple[float,float,float,float]:
    mean,std=mean_std(values);se=std/sqrt(len(values));return mean,std,mean-z*se,mean+z*se

def _percentile(sorted_values:Sequence[float],probability:float)->float:
    position=(len(sorted_values)-1)*probability;low=floor(position);high=min(low+1,len(sorted_values)-1);weight=position-low
    return sorted_values[low]*(1-weight)+sorted_values[high]*weight

def bootstrap_mean_ci(values:Sequence[float],resamples:int=5000,seed:int=20260728,confidence:float=.95)->tuple[float,float,float]:
    if not values or resamples<=0 or not 0<confidence<1:raise ValueError("invalid bootstrap parameters")
    rng=Random(seed);n=len(values);means=sorted(sum(rng.choice(values) for _ in range(n))/n for _ in range(resamples));alpha=1-confidence
    return sum(values)/n,_percentile(means,alpha/2),_percentile(means,1-alpha/2)
