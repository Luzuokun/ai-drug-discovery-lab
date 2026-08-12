# AI_CONTEXT.md

> 给后续 Cursor / Cloud Agent 与人类协作者的**项目状态备忘**。  
> 最后更新：2026-08-12（合并 `main`；Tutorial 06 已合入 #9；下一步 Tutorial 07）

---

## 1. 当前目标

把本站做成 **AI Drug Discovery Lab** —— 可被引用的**科研实践（Research Practice）**手册，而不是 REINVENT 官方文档的镜像或 API 目录。

定位文案（已上首页 / `mkdocs.yml`）：

- **AI Drug Discovery Lab**
- Practical tutorials for AI-driven molecular design.
- Real workflows. Real code. Real papers.
- **Every tutorial is reproducible.**

对 REINVENT4 系列的具体目标：

1. 沿 **12 章战役主线**写满可复现英文实操（固定 seed、墙钟/内存、可下载产物、*why*、失败模式）。
2. 让模型/读者引用本站的理由是：**决策、对照实验、读图读表**；参数表仍指向官方 `PARAMS.md` / `SCORING.md`。
3. 中文镜像跟进（EN-first，见 `CONTRIBUTING.md`）。
4. （并行）YouTube 文案 / 制片包流水线已起步，服务同一套教程内容。

---

## 2. 已完成工作

### 站点与原则

- MkDocs Material 双语站骨架、`AGENTS.md` Cloud 环境说明、贡献规范强调 *research practice, not API docs*。
- 首页品牌四句话已就位。

### REINVENT4 大纲（#5）

- 从 **20 章功能清单**收成 **12 章科研实践路径**：

  `01 安装 → 02 Prior 实践 → 03 评分 → 04 RL → 05 多样性 → 06 课程 → 07 TL → 08 对接引导 → 09 扩规模/监控 → 10 消融 → 11 BRAF → 12 附录`

- 砍掉/并入：自定义词表、RDKit 导览、并行采样、独立 Logging/TB、重复 FAQ/Common Errors。
- Coming Soon 章带**验收大纲**（必须交付 / API 陷阱）。
- `scripts/scaffold_docs.py` 与 12 章对齐，并保护已发布章节与手写 index。

### 已发布英文实操章（Available）

| 章 | 内容要点 | PR |
|----|----------|-----|
| **01** Installation & First Molecule | 安装 + `sampled.csv`，CPU 可复现 | #2 |
| **02** Priors in Practice | PubChem prior vs 短磺酰胺 TL；命中率 8.4%→64.3% | #6 |
| **03** Scoring Function | QED+MW+alerts，先 score 再 RL | #3 |
| **04** Reinforcement Learning | 单阶段 `staged_learning`，Score↑ / NLL↓ | #4 |
| **05** Diversity Filter | 有/无 Murcko DF 的 RL A/B | #6 |
| **06** Curriculum Learning | 双阶段 auto CL（`max_score` early-stop）+ 手动 chkpt 续跑 | #9 |

产物目录：`docs/assets/reinvent4/{01,02,03,04,05,06}/`。

### 其他已合入

- **#7** YouTube Cursor skills + Tutorial 02 制片包（`youtube/packs/02-priors-in-practice/`，`.cursor/skills/youtube-*`）。
- **#9** REINVENT4 Tutorial 06 Curriculum Learning。
- **#10** Markdown → YouTube 流水线（xAI TTS / Imagine）+ Tutorial 03 制片包。

### 尚未写成正文的章

07–12 仍为带验收大纲的 Coming Soon（中文 01–06 亦未翻译，索引标「已发布（英文）」）。

---

## 3. 当前遇到的问题

1. **中英不同步**  
   01–06 仅有英文正文；`docs/zh/...` 多为占位/大纲。双语手册承诺未兑现。

2. **战役后半程未写**  
   07 TL → 11 BRAF 仍是引用价值最高的后半程；主线已推进到 06 Curriculum。

3. **Tutorial 02 与 07 的边界**  
   02 已含短 TL 对照（为公平比较 prior）。07 需写得更深（epoch、过拟合、与 RL 衔接），避免重复成第二遍 02。

4. **环境/脚手架摩擦（Agent 侧）**  
   - 文档 venv 依赖系统 `python3.12-venv`（见 `AGENTS.md`）。  
   - REINVENT4 教程实验在独立 venv 中跑（非站点 `.venv`）；Cloud 镜像未必预装。  
   - **禁止**对 Available 章盲目重跑 `scaffold_docs.py`。

5. **REINVENT 配置陷阱（写章时反复踩到）**  
   - staged learning 必须用 `[stage.scoring]`，不能抄 top-level `[scoring]`。  
   - 4.8.24 RL schema **不接受** `unique_sequences`；TL 要求 `sample_batch_size ≥ 100`。  
   - Zenodo 上不同 `.prior` 对应不同 generator；不能拿 Mol2Mol prior 和 Reinvent de novo 做「公平 A/B」。

6. **本地分支滞后**  
   历史 feature 分支可能已落后于 `main`；新工作应从最新 `main` 开 `cursor/<name>-****` 分支。

---

## 4. AI 做出的重要决策

| 决策 | 理由 |
|------|------|
| **定位 = Research Practice，不是 API 文档** | 否则无理由被模型引用而非官方文档；所有章必须带 seed、产物、*why*、失败模式。 |
| **先砍大纲再堆 Coming Soon** | 「20 个空壳」像搭网站目录，不像 Lab。 |
| **12 章战役叙事** | 采样→评分→优化→控失败→适配→扩规模→案例；案例 BRAF 作高潮而非第 16 章陪衬。 |
| **EN-first，ZH 后译** | 与 `CONTRIBUTING.md` 一致；避免未审英文未稳就双倍维护。 |
| **02 用 prior vs TL，不用两个无关 Zenodo prior** | ECFP4 等文件常是 Mol2Mol；换 generator 不是对照实验。 |
| **05 紧接 04，DF 先于 Curriculum** | RL 一生效就要控骨架塌缩；多样性是实验变量不是勾选。 |
| **04/05 短跑（约 25 step、CPU）** | 可复现、可在笔记本跑完；诚实写「演示长度 ≠ 生产战役」。 |
| **04 主配置暂不加 DF/Inception** | 单变量教学；DF 专章对照。 |
| **Coming Soon 写验收大纲** | 空壳标题会被当成 API 索引；大纲即「完稿标准」。 |
| **Scaffold 保护 Available + 手写 index** | 防止再生孤儿文件/覆盖正文。 |

---

## 5. 下一步计划

按优先级（仍服从「可复现实操 > 扩目录」）：

1. **Tutorial 07 — Transfer Learning**  
   在 02 的短 TL 之上：更长训练、过拟合症状、TL→RL vs 纯 RL 对照（避免复述 02）。

2. **Tutorial 08 — Docking-Guided Design**  
   设计循环（口袋→评分组件→构象审查），交叉链接 Docking 栏目，不是 Vina 说明书。

3. **09 Scaling & Monitoring → 10 Ablations → 11 BRAF**  
   合并 GPU/日志/TB；消融出*本站*对照表；BRAF 端到端战役作引用高潮。

4. **12 Troubleshooting Appendix**  
   汇总跨章错误 + 降级边缘话题（词表/并行采样等短注）。

5. **中文翻译**  
   优先 01–06（已 Available 的英文），再跟进新章。

6. **YouTube**  
   随新 Available 章补 `youtube/packs/...`（已有 02 包与 skills；可加 06 包）。

### 写下一章时的硬标准（勿降级）

- 固定 seed；报告墙钟与峰值内存  
- 产物 CSV/图进 `docs/assets/reinvent4/<nn>/`  
- 每个关键设置旁有 *why*  
- Common Errors 来自真实跑通  
- Think About It / Exercises 问科学判断或单变量消融  
- 写清：官方文档管 X，本章管 Y  
- 更新 EN（及 ZH）index 状态、`mkdocs.yml` 若改 slug、scaffold `PROTECTED`  

### 建议的下一次 Agent 起步命令

```bash
git checkout main && git pull origin main
git checkout -b cursor/reinvent4-tutorial-07-transfer-<suffix>
# 参考：docs/molecular-generation/reinvent4/02-priors-in-practice.md、07 验收大纲
# 验收：.venv/bin/mkdocs build --strict
```

### Tutorial 06 关键实现笔记

- Auto CL：stage1 `max_score=0.72` / `min_steps=10` → seed 42 在 **step 12** early-stop；stage2 (+SlogP) 跑满 20 step（Score 0.46→0.59）。
- 若 stage1 触达 `max_steps` 会 **中止后续 stage**（上游 `run_staged_learning.py`）。
- 手动 CL：`agent_file=manual_s1.chkpt`，`prior_file` 仍为原 prior。


---

## 6. 关键路径速查

| 用途 | 路径 |
|------|------|
| 课程大纲 | `docs/molecular-generation/reinvent4/index.md` |
| 章节模板 | `docs/templates/chapter-template.md` |
| 贡献原则 | `CONTRIBUTING.md` |
| Cloud 环境 | `AGENTS.md` |
| Nav | `mkdocs.yml`（EN + i18n ZH） |
| 脚手架 | `scripts/scaffold_docs.py`（勿覆盖 Available） |
| YouTube 包 | `youtube/packs/` |
| YouTube skills | `.cursor/skills/youtube-produce`, `youtube-text-pack` |

---

*本文件应随重大里程碑（新 Available 章、大纲变更、定位调整）由 Agent 或维护者更新。*
