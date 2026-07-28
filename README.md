# 二进制矩阵重构建模项目

本项目针对游程编码约束下的二进制矩阵恢复问题，提供可验证的基线求解器、CSP约束传播与MRV求解器、完整解空间分析，以及多解空格数量期望的蒙特卡洛实验。

## 项目状态

- [x] 阶段1：游程编码与候选模式生成
- [x] 阶段2：可穷尽的基线求解器
- [x] 阶段3：Excel读取、问题一恢复与行列验证
- [x] 阶段4：问题二完整解空间与不确定格分析
- [x] 阶段5：CSP约束传播与MRV优化
- [x] 阶段6：问题三正式蒙特卡洛实验
- [x] 阶段6C：Bootstrap统计完善
- [x] 阶段7：最终复现与交付验收

## 方法概览

对长度为 `n` 的一行，先根据游程编码生成全部候选0-1序列。矩阵求解被表示为行候选域和列候选域之间的约束满足问题：

1. 删除在对应列或行中没有支持的候选模式；
2. 重复传播直到定义域稳定；
3. 若定义域未唯一化，使用MRV选择候选最少的行或列分支；
4. 对问题一证明唯一，对问题二完整枚举；
5. 对问题三使用固定黑格数量的随机矩阵，精确计算多解空格数。

若解空间为 `S`，格子 `(i,j)` 的上下界为：

```text
L_ij = min X_ij, X in S
U_ij = max X_ij, X in S
```

当 `L_ij != U_ij` 时，该格为多解空格。问题三估计：

```text
E[B | rho]
E[B | rho, solution_count > 1]
```

其中唯一解样本定义 `B=0`。

## 环境

- Python 3.11+
- `openpyxl`：附件读取和结果工作簿
- `numpy/pandas/matplotlib`：实验分析依赖
- 测试基于标准库 `unittest`，安装 `pytest` 后也可发现并运行

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## 问题一

```bash
python -m scripts.solve_problem1 data/附录1-B题数据.xlsx \
  --output-dir outputs/problem1
```

输出 `problem1_results.xlsx` 和 `problem1_summary.json`。

## 问题二

```bash
python -m scripts.solve_problem2 data/附录1-B题数据.xlsx \
  --output-dir outputs/problem2
```

输出完整解、公共矩阵、不确定格数量和1-based坐标。

## 问题三正式实验

固定黑格数量：

```text
K = round(rho * n * n)
```

从 `n*n` 个位置中无放回抽取 `K` 个位置填1。因此实际比例严格等于目标比例，而不是逐格独立Bernoulli抽样。

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

Bootstrap统计完善：

```bash
python -m scripts.bootstrap_problem3 \
  outputs/problem3/formal_results.csv \
  --output-dir outputs/problem3 \
  --resamples 5000 \
  --seed 20260728
```

## 已验证结果

- 问题一四组实例均为唯一解；
- 问题二三组解数量分别为 `2、1、3`，不确定格数为 `4、0、8`；
- 问题三正式实验包含19个比例、每个比例200次，共3800次；
- `E[B|rho]` 的离散峰值位于 `rho=0.20`，均值为 `72.21`；
- 峰值Bootstrap 95%区间为 `[69.555,74.725]`；
- 首个观测到唯一解概率不低于50%的网格点为 `rho=0.50`，概率为 `54.5%`。

## 目录

```text
src/       核心编码、求解、验证、统计模块
tests/     自动化测试
scripts/   问题一、二、三运行入口
outputs/   本地生成结果，不提交实验大文件
data/      本地原始附件，不提交仓库
docs/      建模、实验与复现说明
```

## 数据与复现约定

- 原始竞赛附件不提交仓库；
- 随机种子、比例、规模和重复次数必须写入结果元数据；
- 问题三主曲线使用无条件期望 `E[B|rho]`；
- 多解条件期望只作为补充，并同时报告有效多解样本数；
- 高比例区域多解样本不足时，不解释其条件期望为稳定规律。
