# REINVENT4 教程 08：把对接放进循环，而不是上一堂 Vina 课

## [0:00–0:12] 开场

QED 很高的分子也可能离口袋八丈远。这一集把基于结构的 oracle 放进生成循环——不是 Vina 命令行课。

## [0:12–0:55] 设计循环

先准备口袋，再接评分组件，再短生成，再审查构象。DockStream 已标过时。我们用 ExternalProcess 调 AutoDock Vina，线上每个字节都看得见。配体用 meeko，受体用 Open Babel。公开口袋：PDB 1IEP，Abl 加伊马替尼。

## [0:55–1:40] 先调试 oracle

和教程 03 一样：先 run_type scoring 再 RL。几何平均：QED 权重 0.3，Vina 权重 1。reverse sigmoid 把大约 -5 到 -12 千卡映射到 0 到 1。exhaustiveness 1 只是冒烟。生产要用更高搜索、多样性过滤和队列。

## [1:40–2:55] 证据

种子 42 的先验池：37 个唯一 SMILES。Vina 原始分从 -12.1 到 -4.6。大约 199 秒。同一盒子里 exhaustiveness 1 的伊马替尼大约 -9.4。原始对接最好的分子 QED 可以很低——几何平均允许不同意。短 RL：5 步乘 batch 8，大约 123 秒，噪声是故意的。它证明回路通了，不证明你有苗头系列。

## [2:55–3:35] 对接何时说谎

盒子错、exhaustiveness 太低、互变异构不对、蛋白链不对——亲和力很好看，构象是胡说。一定要把顶部 PDBQT 叠在受体上看。Score 0.0 常常是 3D 嵌入或 Vina 失败。保留 QED 或 alerts，免得发明一堆油腻砖头。

## [3:35–4:00] 结尾

口袋文件、ExternalProcess 脚本和 CSV 在 AI Drug Discovery Lab 网站。代码在 GitHub。下一集教程 09：给昂贵 oracle 扩规模和监控。
