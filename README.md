# Tri-weekly.skill
A Claude Code based skill for tri-weekly academic research papers and consulting reports collection
# 三周报自动化Skill (Copyright © Jinghao Guo 2026)

一个**半自动**的三周报制作技能（**但同时也将功能扩展至OBHRM领域各类相关子模块最新发表/企业实践/业界趋势报告情况梳理，可按需呈教授使用**）：按三周一期的节奏，把 **AI×人力资源、以及 OBHRM 各细分主题**领域的最新学术文献与权威咨询/业界报告，**检索 → 去重 → 归类 → 写中文摘要 → 生成统一格式 Word 文档**。运行在 **Claude Code**（也兼容 Codex / Antigravity 等支持 Agent Skills 的工具）。

---

## 一、它能做什么、产出什么

产出一份 `Volume_2_Issue_N_三周报_YYYYMMDD.docx`：
- 文件开头即**目录**（带点引线和自动页码）；
- 正文按 **自定义的板块**分组；
- 每条 = **中文标题 + 中文摘要 + 【原文信息】引文**；
- 格式复刻既有模板（宋体/Cambria、正文 12pt、行距 1.16、段后 8pt、摘要两端对齐等）。

## 二、边界：Human-in-the-loop，不是全自动（务必先理解）

- Claude **不会定时运行、不会主动提醒**，每期由人手动触发。
- 学术检索靠 **Crossref（确定、穷尽）** + 联网搜索（补咨询/业界报告）；**微信公众号/小红书资源无法自动枚举**，需手动上传、Claude 回溯到其引用的原始论文。
- **人保留三处把关**：① 确认检索窗口；② 上传社媒；③ 终审选题。
- 摘要**只据取到的原文写、不臆造数字**；取不到全文会标"仅据摘要"，需人工复核。

## 三、环境准备（每台机器一次）

1. **装 Claude Code**（原生安装器，无需 Node.js）：
   - macOS/Linux：`curl -fsSL https://claude.ai/install.sh | bash`
   - Windows（PowerShell）：`irm https://claude.ai/install.ps1 | iex`
2. **Python + python-docx**（生成 docx 用）：`pip install python-docx`
   - **Windows + Anaconda 常见坑**：若敲 `python` 弹出微软商店，说明撞上了占位 stub。解决：用 Anaconda 的**全路径**调脚本（例 `F:\Anaconda\python.exe scripts\generate_docx.py ...`），或关掉"应用执行别名"中的 `python.exe/python3.exe` 并在 Anaconda Prompt 跑 `conda init` 后重开终端。
3. 检索脚本需本机**联网到 api.crossref.org**。

## 四、安装技能

把本仓库放到 Claude Code 的技能目录，使该目录下直接有 `SKILL.md`、`scripts/`、`references/`：
- 个人（所有项目可用）：`~/.claude/skills/sanzhoubao/`
- 推荐直接克隆：`git clone <仓库地址> ~/.claude/skills/sanzhoubao`
- Codex / Antigravity 放 `.agents/skills/sanzhoubao/`。

重开一个会话，Claude Code 会自动识别。

## 五、怎么用（一期完整流程）

1. **触发**：跟 Claude 说"做第 N 期三周报"。
2. **确认窗口**：Claude 自报期号 / 目标日 / 检索窗口，你确认或调整。
3. **报本期主题 + 板块**：AI×OBHRM（默认），或其他 OBHRM 主题（组织变革 / 招聘甄选 / 薪酬 / 绩效 / 团队动力学…）；并给本期板块清单（可自拟、数目不限，不报则用默认）。
4. **检索**：Claude 跑 Crossref 拉 A 类全量候选 + 抓咨询/业界报告。
5. **上传社媒**：Claude 停下，上传微信公众号 / 小红书等资源（没有即回复"无"）；它回溯到原始论文再纳入。
6. **评审**：Claude 给每条"主旨 + 入选理由 + 置信度"，手动定边缘条目留/删、新来源批/不批。
7. **生成**：Claude 写摘要、排版、出 docx。
8. **收尾**：用 Word 打开，**Ctrl+A → F9** 刷新目录页码。

## 六、换主题 / 临时加刊

- **换主题**：第 3 步直接报即可（通用档 `references/themes/obhrm_generic.md` 承接），无需改文件。常做的主题可在 `references/themes/` 下建专门档补锚点示例，分类更准。
- **临时加一两本刊**：用脚本参数保持确定性——
  ```
  python scripts/fetch_candidates.py <窗口起> <窗口止> --mailto 你的邮箱 \
      --add "Compensation & Benefits Review" --add 1468-2389
  ```
  刊名有歧义时**优先填 ISSN**（如 `1468-2389` = International Journal of Selection and Assessment）。常用的就固化进 `references/journals_a_tier.txt`。

## 七、期刊白名单（检索范围）

四层（详见 `references/source_registry.md`）：
- **A-1** FT50 中管理/OB/HRM/战略/IS/创业相关刊；
- **A-2** ABS/AJG 2024 六个相关学科组的 4*/4 头部刊；
- **A-3** AI×工作 / 跨学科（往期高频）；
- **A-4** 具名补充（规则外、口碑好的刊）。

**选取规则**：FT50 ∪ AJG(ABS)2024 在六组（创业、综合管理与伦理、HRM 与雇佣、组织研究、组织心理、战略）的 4*/4/3 ∪ 往期已出现刊物。
`references/journals_a_tier.txt` 是检索脚本实际查询的刊名清单。

## 八、去重总账（团队共享的关键）

`references/dedup_ledger.json` 是**累积总账**：每期定稿后把全部【原文信息】追加进去，下期对**全部历史**去重（DOI > 标题 > URL，并做工作论文 vs 正式发表的跨版本归并）。

**团队协作约定**：
- 开工前 `git pull` 拿最新总账；
- 定稿后 `git commit` + `git push` 回仓库；
- **同一期由一人主理**，避免覆盖（总账为"最后写入覆盖"）。

## 九、仓库结构

```
sanzhoubao/
├── SKILL.md                      # 技能入口：触发条件 + 8 节点工作流 + 格式规范表
├── README.md                     # 本说明
├── scripts/
│   ├── compute_window.py         # 自报日期：算期号/目标周五/检索窗口
│   ├── fetch_candidates.py       # Crossref 按刊名/ISSN+日期 确定性穷尽拉取候选
│   └── generate_docx.py          # 按模板规格生成 docx
└── references/
    ├── source_registry.md        # A/A2/B/C 四层来源白名单 + 选取规则
    ├── journals_a_tier.txt        # 检索脚本用的 A 类刊名清单
    ├── inclusion_rubric.md       # 收录四道闸 + 板块锚点 + 摘要主旨保真规则
    ├── dedup_ledger.json         # 累积去重总账（每期追加）
    ├── issue_schema.example.json # 生成器输入格式样例
    ├── sample_output_第9期_demo.docx  # 格式样张
    └── themes/                   # 主题档：ai_obhrm.md（默认）/ obhrm_generic.md（通用）/ _template.md
```

## 十、已知限制

- **召回有索引滞后**：最新 1~2 周文献可能尚未入 Crossref，故窗口结束日留约 1 周缓冲，跨期不留空档补上。
- **web_search 部分非确定/不穷尽**：A 类靠 Crossref 才能确定且拉全；社媒、咨询报告无法穷尽。
- **HITL**：每期需人触发并在三处把关。
- 摘要严格忠于原文、不编造统计量；社媒解读与原文冲突时以原文为准。
