# AI_CONTEXT.md

> 给后续 Cursor / Cloud Agent 与人类协作者的**项目状态备忘**。  
> 最后更新：2026-08-18（REINVENT4 Tutorials 09–12 英文实操 Available；12 章战役英文主线写完）

---

## 1. 当前目标

把本站做成 **AI Drug Discovery Lab** —— 可被引用的**科研实践（Research Practice）**手册，而不是 REINVENT 官方文档的镜像或 API 目录。

定位文案（已上首页 / `mkdocs.yml`）：

- **AI Drug Discovery Lab**
- Practical tutorials for AI-driven molecular design.
- Real workflows. Real code. Real papers.
- **Every tutorial is reproducible.**

对 REINVENT4 系列的具体目标：

1. 沿 **12 章战役主线**写满可复现英文实操（固定 seed、墙钟/内存、可下载产物、*why*、失败模式）。**英文 01–12 已 Available。**
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
| **07** Transfer Learning | 40-epoch TL 过拟合曲线；TL→RL vs RL-only（同评分） | #11 |
| **08** Docking-Guided Design | 1IEP 口袋 + ExternalProcess Vina；scoring + 短 RL + 构象审查 | #11 |
| **09** Scaling & Monitoring | 同 T04 协议 + TensorBoard；TB on/off 化学一致；CPU 无 GPU 诚实记录 | （本 PR） |
| **10** Ablations | `sigma` 64/128/256 seed 42；推荐默认 128 | （本 PR） |
| **11** Case Study: BRAF | 配体相似性战役；预注册成功标准；25 vs 80 step | （本 PR） |
| **12** Troubleshooting Appendix | 错误索引 + 词表/并行/RDKit 短注；不另开 FAQ 导航 | （本 PR） |

产物目录：`docs/assets/reinvent4/{01,…,12}/`（12 无实验图，索引章）。

### 其他已合入

- **#7** YouTube Cursor skills + Tutorial 02 制片包。
- **#9** REINVENT4 Tutorial 06 Curriculum Learning。
- **#10** Markdown → YouTube 流水线 + Tutorial 03 制片包。
- **#12** Tutorials 01–08 YouTube Discovery 草稿。

### 尚未写成正文的工作

- **中文翻译**：01–12 英文已齐；`docs/zh/...` 对 Available 章标「已发布（英文）」。
- **YouTube Discovery**：09–12 尚未出包。

---

## 3. 当前遇到的问题

1. **中英不同步**  
   01–12 仅有英文正文；`docs/zh/...` 多为占位/大纲。双语手册承诺未兑现。

2. **Tutorial 02 与 07 的边界（已处理）**  
   02 = 短 TL 对照 prior；07 = 更长训练、过拟合、TL→RL A/B。勿再写成第二遍 02。

3. **环境/脚手架摩擦（Agent 侧）**  
   - 文档 venv 依赖系统 `python3-venv` / `python3.12-venv`（见 `AGENTS.md`）。  
   - REINVENT4 教程实验在独立 venv 中跑（非站点 `.venv`）；Cloud 镜像未必预装 GPU。  
   - 对接章另需 `autodock-vina`、`openbabel`、`meeko`(+`gemmi`)。  
   - **禁止**对 Available 章盲目重跑 `scaffold_docs.py`。

4. **REINVENT 配置陷阱（写章时反复踩到）**  
   - staged learning 必须用 `[stage.scoring]`，不能抄 top-level `[scoring]`。  
   - 4.8.24 RL schema **不接受** `unique_sequences`；TL 要求 `sample_batch_size ≥ 100`。  
   - Zenodo 上不同 `.prior` 对应不同 generator；不能拿 Mol2Mol prior 和 Reinvent de novo 做「公平 A/B」。  
   - TL 每个 epoch 会覆盖裸 `output_model_file`；中间档为 `*.N.chkpt`。  
   - DockStream 已标 superseded；教学对接用 ExternalProcess + Vina 更透明。  
   - `tb_logdir = "tb_rl"` 实际写到 `tb_rl_0/`（staged learning 追加 `_{run}`）。  
   - CPU wheel 上 `device = "cuda:0"` → `Torch not compiled with CUDA enabled`。  
   - 本协议下 `scoring.parallel=4` 比 `1` **更慢**（RDKit 太便宜）。

5. **本地分支滞后**  
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
| **07 故意 40 epoch 过拟合** | 在同一小集上展示 mem%/scaffold 塌缩；最佳 val NLL = ep 8。 |
| **07 TL→RL 用 ep24 + 两边都指 TL chkpt** | 同评分隔离 TL 效应；DAP prior 必须是适配后的分布。 |
| **08 ExternalProcess+Vina，不用 DockStream** | 教学可调试；DockStream superseded；交叉链接 Docking 栏目。 |
| **08 短 RL 诚实写噪声** | 5×8@exh=1 只证明回路通，不宣称优化成功。 |
| **09 无 GPU 仍写扩规模** | 同 seed TB on/off 证明化学不变；GPU 作为一行 TOML + CPU-wheel 真失败；吞吐用 mol/s。 |
| **10 只消融 sigma** | 25 step / 1 seed 下 rate 不可辨；batch 已在 09 当吞吐变量。 |
| **11 配体相似性而非 BRAF 对接** | 对接需另建口袋（08 是 Abl 1IEP）；预注册标准 + QED-RL 对照；诚实写 Tc 0.20 仍 analog-remote。 |
| **12 只做索引** | 不复活独立 FAQ 导航；词表/并行/RDKit 短注。 |
| **Coming Soon 写验收大纲** | 空壳标题会被当成 API 索引；大纲即「完稿标准」。 |
| **Scaffold 保护 Available + 手写 index** | 防止再生孤儿文件/覆盖正文。 |

---

## 5. 下一步计划

按优先级（仍服从「可复现实操 > 扩目录」）：

1. **中文翻译**  
   优先 01–08，再 09–12。索引已标「已发布（英文）」。

2. **YouTube Discovery（01–08 草稿已齐；09–12 未出）**  
   `youtube/packs/<slug>/` 文案 + xAI Imagine 静帧 + xAI TTS（gitignored `youtube/audio/`）+ ffmpeg `youtube/renders/<slug>/draft.mp4`（gitignored）。

3. **BRAF 对接 follow-up（练习，非新章）**  
   Tutorial 11 Challenge：对 BRAF 共晶（非 1IEP）重复 08 的 ExternalProcess+Vina 协议。

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
git checkout -b cursor/reinvent4-zh-01-<suffix>
# 优先翻译 docs/molecular-generation/reinvent4/01–04
# 验收：.venv/bin/mkdocs build --strict
```

### Tutorial 09 关键实现笔记

- 主机：4-core Xeon，PyTorch **2.12.0+cpu**，无 `nvidia-smi`。
- T04 协议 seed 42：Score **0.66→0.79**，Agent NLL **34.79→27.15**（与 T04 化学一致）。
- TB off **61.2 s** / on **66.6 s**（+9%）；step-1 SMILES 完全相同。
- `tb_logdir = "tb_rl"` → 目录 `tb_rl_0/`。
- batch 32：33.4 s、800 mol、~23.9 mol/s（vs 64 的 26.1）；RAM 1.23 vs 1.51 GiB。
- `scoring.parallel=4`（10 step）**55.7 s** vs parallel=1 **31.0 s**。
- CUDA TOML：`AssertionError: Torch not compiled with CUDA enabled`。

### Tutorial 10 关键实现笔记

- `sigma` 64 / 128 / 256，同 seed、同 25×64。
- Score@25：0.77 / **0.79** / 0.77；Valid@25：100 / 100 / **98%**。
- Unique Murcko：1225 / 1164 / 1216。推荐默认 **128**。
- 下一步不调：`rate`（需多种子）、与 batch 同时网格。

### Tutorial 11 关键实现笔记

- 参考：vemurafenib；Morgan r=2 counts；几何平均 + QED + MW 200–500 + alerts + Murcko DF。
-  Sanity：vemurafenib Tc=1.0、QED=0.35、Score=0.69；benzene Tc=0.06；dabrafenib MW 520。
- T04 step25 再打 BRAF 分：mean Tc **0.12**。
- BRAF-RL 25 step：Tc 0.137→0.150；80 step：→**0.196**（Δ+0.059）。
- 末批 7-azaindole **0/64**。不宣称 BRAF 活性。

### Tutorial 07 关键实现笔记

- 同 Tutorial 02 sulfonamide 集；40 epoch，`save_every_n_epochs=8`。
- Best validation loss **39.395 @ epoch 8**。
- Mem %：ep8=0 → ep24=12 → ep40=40；scaffolds 168→139；unique rows 191→165。
- TL→RL（ep24 作 prior+agent）last5 Score **0.847** / sulfa **66.6%** vs RL-only **0.775** / **4.4%**。

### Tutorial 08 关键实现笔记

- 口袋：PDB **1IEP** chain A + STI；`box.txt` 约 30 Å。
- Oracle：`ExternalProcess` → `vina_external.py`（meeko 配体 PDBQT）。
- Pool scoring n=37：Vina raw **−12.1…−4.6**；~199 s。
- RL：batch 8 × 5 step，exh=1；~123 s；曲线噪声大 —— 正文如实写。

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
