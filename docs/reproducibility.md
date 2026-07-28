# 复现实验说明

## 1. 环境与数据

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

将竞赛附件放在本地 `data/附录1-B题数据.xlsx`。原始附件不提交公开仓库。

## 2. 自动测试

```bash
python -m compileall -q src tests scripts
python -m unittest discover -s tests -v
```

## 3. 问题一

```bash
python -m scripts.solve_problem1 data/附录1-B题数据.xlsx --output-dir outputs/problem1
```

验收不变量：四组均为唯一解，基线节点数为 `17、23、25、97`，所有行列验证通过。

## 4. 问题二

```bash
python -m scripts.solve_problem2 data/附录1-B题数据.xlsx --output-dir outputs/problem2
```

验收不变量：解数量为 `2、1、3`，多解空格数为 `4、0、8`。

## 5. CSP交叉验证

```bash
python -m scripts.benchmark_solvers data/附录1-B题数据.xlsx
```

基线与CSP完整解集必须相同。

## 6. 问题三正式实验

```bash
python -m scripts.run_problem3_pilot \
  --n 10 \
  --ratios 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 \
           0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 \
  --trials 200 --seed 20260727 --prefix formal --formal \
  --output-dir outputs/problem3
```

应生成3800条记录。`E[B|rho]`峰值网格点为 `rho=0.20`，均值72.21；`rho=0.50`唯一解概率为0.545。运行时间因机器而异，不用于文件哈希验证。

## 7. Bootstrap统计

```bash
python -m scripts.bootstrap_problem3 \
  outputs/problem3/formal_results.csv \
  --output-dir outputs/problem3 \
  --resamples 5000 --seed 20260728
```

峰值Bootstrap 95%区间应为 `[69.555,74.725]`。固定随机种子下结果可逐值复现。

## 8. 统计口径

- `B`为全部可行解中取值不固定的格子数量；
- 唯一解样本取 `B=0`；
- 主指标为 `E[B|rho]`；
- 条件指标为 `E[B|rho, solution_count>1]`；
- 多解样本少于30时标记为样本不足；
- 没有多解样本时条件期望未定义，不记为0；
- 随机矩阵固定1的总数量 `K=round(rho*n*n)`，不得与逐格Bernoulli抽样混用。
