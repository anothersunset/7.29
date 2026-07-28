"""Statistical summaries for Monte Carlo reconstruction experiments."""
from __future__ import annotations
from math import sqrt
from collections.abc import Sequence
def wilson_interval(successes:int,total:int,z:float=1.959963984540054)->tuple[float,float]:
    if total<=0 or not 0<=successes<=total:raise ValueError("invalid binomial counts")
    p=successes/total;d=1+z*z/total;center=(p+z*z/(2*total))/d;margin=z*sqrt(p*(1-p)/total+z*z/(4*total*total))/d;return max(0.0,center-margin),min(1.0,center+margin)
def mean_std(values:Sequence[float])->tuple[float,float]:
    if not values:raise ValueError("values must not be empty")
    mean=sum(values)/len(values)
    if len(values)==1:return mean,0.0
    return mean,sqrt(sum((x-mean)**2 for x in values)/(len(values)-1))
def mean_ci95(values:Sequence[float],z:float=1.959963984540054)->tuple[float,float,float,float]:
    mean,std=mean_std(values);se=std/sqrt(len(values));return mean,std,mean-z*se,mean+z*se
