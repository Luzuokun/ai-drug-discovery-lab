# AI_CONTEXT.md

> 给后续 Cursor / Cloud Agent 与人类协作者的**项目状态备忘**。  
> 最后更新：2026-08-14（Tutorial 07/08 英文实操 Available + REINVENT4 01–08 YouTube Discovery 草稿）

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
| **07** Transfer Learning | 40-epoch TL 过拟合曲线；TL→RL vs RL-only（同评分） | （本 PR） |
| **08** Docking-Guided Design | 1IEP 口袋 + ExternalProcess Vina；scoring + 短 RL + 构象审查 | （本 PR） |

产物目录：`docs/assets/reinvent4/{01,…,08}/`。

### 其他已合入

- **#7** YouTube Cursor skills + Tutorial 02 制片包（`youtube/packs/02-priors-in-practice/`，`.cursor/skills/youtube-*`）。
- **#9** REINVENT4 Tutorial 06 Curriculum Learning。
- **#10** Markdown → YouTube 流水线（xAI TTS / Imagine）+ Tutorial 03 制片包。

### 尚未写成正文的章

09–12 仍为带验收大纲的 Coming Soon（中文 01–08 亦未翻译，索引标「已发布（英文）」）。

---

## 3. 当前遇到的问题

1. **中英不同步**  
   01–08 仅有英文正文；`docs/zh/...` 多为占位/大纲。双语手册承诺未兑现。

2. **战役后半程**  
   09 Scaling → 11 BRAF 仍是引用价值最高的后半程高潮未写。

3. **Tutorial 02 与 07 的边界（已处理）**  
   02 = 短 TL 对照 prior；07 = 更长训练、过拟合、TL→RL A/B。勿再写成第二遍 02。

4. **环境/脚手架摩擦（Agent 侧）**  
   - 文档 venv 依赖系统 `python3-venv` / `python3.12-venv`（见 `AGENTS.md`）。  
   - REINVENT4 教程实验在独立 venv 中跑（非站点 `.venv`）；Cloud 镜像未必预装。  
   - 对接章另需 `autodock-vina`、`openbabel`、`meeko`(+`gemmi`)。  
   - **禁止**对 Available 章盲目重跑 `scaffold_docs.py`。

5. **REINVENT 配置陷阱（写章时反复踩到）**  
   - staged learning 必须用 `[stage.scoring]`，不能抄 top-level `[scoring]`。  
   - 4.8.24 RL schema **不接受** `unique_sequences`；TL 要求 `sample_batch_size ≥ 100`。  
   - Zenodo 上不同 `.prior` 对应不同 generator；不能拿 Mol2Mol prior 和 Reinvent de novo 做「公平 A/B」。  
   - TL 每个 epoch 会覆盖裸 `output_model_file`；中间档为 `*.N.chkpt`。  
   - DockStream 已标 superseded；教学对接用 ExternalProcess + Vina 更透明。

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
| **07 故意 40 epoch 过拟合** | 在同一小集上展示 mem%/scaffold 塌缩；最佳 val NLL = ep 8。 |
| **07 TL→RL 用 ep24 + 两边都指 TL chkpt** | 同评分隔离 TL 效应；DAP prior 必须是适配后的分布。 |
| **08 ExternalProcess+Vina，不用 DockStream** | 教学可调试；DockStream superseded；交叉链接 Docking 栏目。 |
| **08 短 RL 诚实写噪声** | 5×8@exh=1 只证明回路通，不宣称优化成功。 |
| **Coming Soon 写验收大纲** | 空壳标题会被当成 API 索引；大纲即「完稿标准」。 |
| **Scaffold 保护 Available + 手写 index** | 防止再生孤儿文件/覆盖正文。 |

---

## 5. 下一步计划

按优先级（仍服从「可复现实操 > 扩目录」）：

1. **Tutorial 09 — Scaling & Monitoring**  
   GPU / 日志 / TensorBoard；服务长战役与贵 oracle（对接）。

2. **10 Ablations → 11 BRAF**  
   消融出*本站*对照表；BRAF 端到端战役作引用高潮。

3. **12 Troubleshooting Appendix**  
   汇总跨章错误 + 降级边缘话题（词表/并行采样等短注）。

4. **中文翻译**  
   优先 01–08（已 Available 的英文），再跟进新章。

5. **YouTube Discovery（01–08 草稿已齐）**  
   `youtube/packs/<slug>/` 文案 + xAI Imagine 静帧 + xAI TTS（gitignored `youtube/audio/`）+ ffmpeg `youtube/renders/<slug>/draft.mp4`（gitignored）。  
   目标 3–5 分钟；剪映插入录屏 → 上传 → 再把 URL 写回 MkDocs。新 Available 章继续补包。

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
git checkout -b cursor/reinvent4-tutorial-09-scaling-<suffix>
# 参考：docs/molecular-generation/reinvent4/08-docking-guided-design.md、09 验收大纲
# 验收：.venv/bin/mkdocs build --strict
```

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
