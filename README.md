# 二进制矩阵重构建模项目

本仓库用于实现基于游程编码约束的二进制矩阵恢复、解空间分析与随机模拟。

## 当前阶段

- [x] 阶段 0：仓库初始化
- [ ] 阶段 1：游程编码与候选模式生成
- [ ] 阶段 2：基线求解器
- [ ] 阶段 3：Excel 读取与问题一
- [ ] 阶段 4：问题二解空间分析
- [ ] 阶段 5：CSP 约束传播与 MRV 优化
- [ ] 阶段 6：问题三蒙特卡洛模拟
- [ ] 阶段 7：交付验收

## 技术约定

- Python 3.11+
- 使用类型标注
- 使用 `pytest` 进行自动化测试
- 原始竞赛附件默认不提交到仓库

## 目录结构

```text
src/       核心源码
tests/     自动化测试
scripts/   各问题运行入口
outputs/   结果输出目录
data/      本地数据目录（原始附件不提交）
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

> 当前仅完成项目骨架，尚未加入业务求解代码。
