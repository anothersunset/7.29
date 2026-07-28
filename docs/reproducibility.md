# 复现实验说明

## 1. 环境

建议使用Python 3.11或更高版本。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows激活命令：

```powershell
.venv\Scripts\activate
```

## 2. 数据文件

将竞赛附件放到本地 `data/` 目录，例如：

```text
data/附录1-B题数据.xlsx
```

原始附件不应提交到公开仓库。

## 3. 自动测试

```bash
python -m compileall -q src tests scripts
python -m unittest discover -s tests -v
```

最终验收应全部通过。

## 4. 问题一

```bash
python -m scripts.solve_problem1 \
  data/附录1-B题数据.xlsx \
  --output-dir outputs/problem1
```

验收不变量：

```text
第一问1：1解，17个基线节点
第一问2：1解，23个基线节点
第一问3：1解，25个基线节点
第一问4：1解，97个基线节点
所有行列验证均通过
```

## 5. 问题二

```bash
python -m scripts.solve_problem2 \
  data/附录1-B题数据.xlsx \
  --output-dir outputs/problem2
```

验收不变量：

```text
第二问1：2解，4个不确定格
第二问2：1解，0个不确定格
第二问3：3解，8个不确定格
```

## 6. CSP与基线交叉验证

```bash
python -m scripts.benchmark_solvers data/附录1-B题数据.xlsx
```

问题一和问题二的完整解集必须满足：

```python
set(baseline.solutions) == set(csp.solutions)
```

## 7. 问题三正式实验

```bash
python -m scripts.run_problem3_pilot \
  --n 10 \
  --ratios 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 \
           0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 \
  --trials 200 \
  --seed 20260727 \
  --prefix formal \
  --formal \
  --output-dir outputs/problem3
```

该命令生成：

```text
formal_results.csv
formal_summary.csv
formal_summary.json
```

正式实验不变量：

```text
记录数：3800
比例数：19
每个比例：200次
E[B|rho]峰值网格点：rho=0.20
峰值均值：72.21
rho=0.50唯一解概率：0.545
```

逐次运行时间会因机器不同而变化，不应将耗时列用于文件哈希验证。

## 8. Bootstrap统计

```bash
python -m scripts.bootstrap_problem3 \
  outputs/problem3/formal_results.csv \
  --output-dir outputs/problem3 \
  --resamples 5000 \
  --seed 20260728
```

输出：

```text
formal_bootstrap_summary.csv
formal_bootstrap_summary.json
```

峰值Bootstrap 95%区间应为：

```text
rho=0.20：[69.555, 74.725]
```

Bootstrap结果使用固定随机种子，可逐值复现。

## 9. 统计口径

- `B`：全部可行解中取值不固定的格子数量；
- 唯一解样本：`B=0`；
- 主指标：`E[B|rho]`；
- 补充指标：`E[B|rho, solution_count>1]`；
- 多解样本数小于30时，条件期望标记为样本不足；
- 没有多解样本时，条件期望记为未定义，不记为0。

## 10. 随机机制

问题三固定1的总数量：

```text
K = round(rho * n * n)
```

随后从全部格子中无放回抽取 `K` 个位置。这与每格独立Bernoulli抽样不同，复现时不得混用。

## 11. 问题四复现

将 `附录2-第四问数据.txt` 放入本地 `data/` 目录，然后运行：

```bash
python -m scripts.solve_problem4 \
  data/附录2-第四问数据.txt \
  --output-dir outputs/problem4
```

验收不变量：

```text
矩阵规模：50×50
完整解数量：24
是否唯一：否
多解空格数：30
搜索节点：59
所有完整解行列验证：通过
```

输出文件：

```text
problem4_summary.json
problem4_results.xlsx
problem4_representative.png
problem4_consensus.png
```

其中代表解图展示一个合法世界地图像素图；公共矩阵图以红色表示24个解之间取值不固定的30个格子。
