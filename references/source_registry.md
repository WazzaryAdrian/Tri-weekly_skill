# 来源登记表 v0.3（白名单 = 检索范围 + 准入闸门）
> 口径：A 类 = FT50 中管理/OB/HRM/战略/信息系统相关刊 ∪ ABS/AJG 2024 在六个相关学科组的 3/4/4* ∪ 往期三周报已出现刊物。白名单为主；不在表内者进"候选隔离区"待批，不直接收。
> **选取规则（可据此扩充）**：纳入 AJG（ABS）2024 评级为 4*/4/3 且属于以下六组的刊物——Entrepreneurship & Small Business；General Management, Ethics, Gender & Social Responsibility；Human Resource Management & Employment Studies；Organization Studies；Psychology (Organizational)；Strategy。该口径约 82 刊，是 OBHRM 跨学科综述的标准取样框。AI×工作议题另保留信息系统(IS)与若干跨学科刊。

## A 类 · 同行评审期刊（主检索范围）

### A-1 FT50 中相关刊（已核对 FT50 2024 全名单，取管理/OB/HRM/战略/IS/创业相关者）
Academy of Management Journal；Academy of Management Review；Administrative Science Quarterly；Human Relations；Human Resource Management (Wiley)；Information Systems Research；Journal of Applied Psychology；Journal of Business Ethics；Journal of International Business Studies；Journal of Management；Journal of Management Information Systems；Journal of Management Studies；Management Science；MIS Quarterly；Organization Science；Organization Studies；Organizational Behavior and Human Decision Processes；Research Policy；Strategic Management Journal；MIT Sloan Management Review；Harvard Business Review；Entrepreneurship Theory and Practice；Journal of Business Venturing。
（FT50 中纯财务/会计/营销/宏观经济刊如 J. Finance、J. Accounting Research、J. Marketing、Econometrica 等，与本主题关系弱，默认不主检索；如某期议题涉及再临时纳入。）

### A-2 ABS/AJG 六组的 4*/4/3 相关刊（FT50 之外的扩充）
> 评级为 AJG 2024 大致口径（个别有 2024 调整，如 Business Ethics Quarterly 由 4 降 3）；建议对官方表抽查。检索实际以 `journals_a_tier.txt` 刊名为准。

**① 组织心理 (Psychology-Organizational)**：Personnel Psychology(4*)；Organizational Behavior and Human Decision Processes(4*)；Organizational Research Methods(4*)；Journal of Organizational Behavior(4)；The Leadership Quarterly(4)；Journal of Vocational Behavior(4)；Journal of Occupational and Organizational Psychology(3/4)；European Journal of Work and Organizational Psychology(3)；Journal of Business and Psychology(3)；Journal of Occupational Health Psychology(3)；Work & Stress(3)；Human Performance(3)。
**② 人力资源/雇佣 (HRM & Employment)**：Human Resource Management Journal(4,UK)；Work, Employment and Society(4)；ILR Review(4)；British Journal of Industrial Relations(4)；International Journal of Human Resource Management(3)；Human Resource Management Review(3)；Industrial Relations: A Journal of Economy and Society(3)。
**③ 综合管理/伦理/性别/社会责任 (Gen Mgmt & Ethics)**：Academy of Management Annals(4*)；British Journal of Management(4)；International Journal of Management Reviews(4)；Journal of Business Ethics(3)；Business Ethics Quarterly(3)；Business & Society(3)；Gender, Work & Organization(3)。
**④ 组织研究 (Organization Studies)**：Organization Studies(4)；Human Relations(4)；Organization(3)；Group & Organization Management(3)；Strategic Organization(4，与战略交叉)。
**⑤ 战略 (Strategy)**：Strategic Entrepreneurship Journal(4)；Global Strategy Journal(3)；Long Range Planning(3)；Business Strategy and the Environment(3)。（SMJ 见 A-1）
**⑥ 创业与小企业 (Entrepreneurship)**：Small Business Economics(4)；Family Business Review(3/4)；Entrepreneurship & Regional Development(3)；International Small Business Journal(3)；Journal of Small Business Management(3)。（JBV、ETP 见 A-1）

### A-3 AI×工作 / 跨学科（往期高频、保留）
Nature Human Behaviour；PNAS；Journal of Business Research；Applied Psychology: An International Review (IAAP)；Journal of Applied Behavioral Science；Marketing Science；Contemporary Accounting Research；AEA Papers and Proceedings；经济研究（中文）。

### A-4 具名补充（规则之外、用户点名纳入的口碑刊）
规则按 FT50+ABS≥3 取，会漏掉部分 ABS 2 但口碑好的区域/专门刊。此处收用户点名者：Asia Pacific Journal of Human Resources（APJHR，ABS≈2/ABDC A）。后续可继续追加。

**质量校验**：须有真实 DOI（Crossref 可查），且刊物在本表内或被 Scopus/WoS/DOAJ 收录。

## A2 类 · 工作论文 / 预印本平台（可收，需额外校验）
SSRN、arXiv、NBER、World Bank Policy Research、高校工作论文（HBS 等）、博士论文。
**校验**：① 作者机构可信；② 是否标注 forthcoming 于 A 类刊/知名会议；③ 有无 DOI。这些是平台不是刊物，不能靠刊名把关。

## B 类 · 权威实务 / 研究机构（直接抓官网"近期发布"；有墙也列、正文留占位）
**范围 = 凡与 HRM 相关、且会发报告的大型咨询/研究机构**，包括但不限于：
- MBB：McKinsey、BCG、Bain
- 四大：Deloitte、PwC、EY、KPMG
- 人力资本专业机构：Korn Ferry、Mercer、WTW、Aon（怡安）、ADP、Gartner、SHRM、Conference Board、WEF、Robert Walters
- 商业/学术媒体：Harvard Business Review、MIT Sloan Management Review、Microsoft（研究/官方）、财经
- 商学院洞见（候选级，可纳）：IMD、INSEAD 等
**规则**：发现报告已 release，即列"标题+日期+链接"，全文有墙则正文写 `〔待手动下载〕`，用户事后补。

## C 类 · 中文社媒（发现层，非独立来源；只能用户提供）
- 微信公众号 / 小红书：本质是对同一批期刊的二手综述。功能 = 帮用户更快定位原始论文。
- 处理：用户贴链接/正文 → Claude **回溯到所引原始期刊文献**，按 A 类收录与去重；社媒链接本身不作最终引文。
- 九期中无小红书先例；公众号 URL 不含账号名，无法反推——**如需固定关注账号清单，由用户提供**。

---
## 主题可切换（见 SKILL.md 节点①的"主题配置"）
上述 A 类与五大板块默认针对 **AI × OBHRM**。换研究主题（如纯战略学）时，在 `references/themes/<主题>.md` 里覆盖：主题闸门关键词、五板块定义、板块锚点示例；A 类刊单与本表大体复用（FT50+ABS 同一取样框）。
