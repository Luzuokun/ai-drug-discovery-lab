# REINVENT4 教程 01：四分钟拿到第一批 AI 分子

## [0:00–0:12] 开场

在你拿到一份真实的 sampled.csv 之前，你还没有生成模型。这一集安装 REINVENT4，并在 CPU、随机种子 42 上用分子证明它能跑。

## [0:12–0:50] 问题

直接 pip install reinvent 行不通。REINVENT4 要克隆仓库，用 install.py 让 PyTorch 匹配 CPU 或 CUDA。Python 需要 3.11 及以上。Prior 不是文件名奖杯，而是会吐出 SMILES 的训练分布。

## [0:50–1:35] 心智模型

三个词。Prior：Zenodo 上冻结的化学大脑，这里是 reinvent_pubchem.prior。Agent：稍后用强化学习微调的可训练副本。词表：写在 prior 文件里的 SMILES 记号。采样只是向 prior 要分子，还没有打分。

## [1:35–2:50] 证据

配置：run_type sampling，CPU，num_smiles 100，unique_molecules 打开，种子 42。手册这次跑大约 3.5 秒，峰值内存约 550 MiB。请求 100 个，4 条无效被丢掉，写出 96 个唯一有效分子。列是 SMILES、SMILES_state、NLL。NLL 最小 21.37，均值 36.44，最大 76.98。NLL 越低，模型越自信。没有 Score 列——采样还没有奖励。

## [2:50–3:35] 失败模式

unique_molecules 为真只是请求，不是保证——重复和无效会在生成后消失。高 NLL 是少见化学，不是崩溃。如果 Score 全是零，那是后续评分配置的问题，不是采样失败。Prior 路径错了或 Zenodo 下到一半，才会找不到文件。

## [3:35–4:00] 结尾

完整安装命令、采样 TOML 和 sampled.csv 在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集：需要选 prior 看教程 02；要接奖励看教程 03。链接在简介里。
