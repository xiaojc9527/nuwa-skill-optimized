# 女娲.skill (优化版)

「你想蒸馏的下一个员工，何必是同事」

## 项目简介

女娲帮你蒸馏任何人的思维方式，让乔布斯、马斯克、芒格、费曼都给你打工。

这是 `nuwa-skill` 项目的优化版本，在保留原有功能的基础上，进行了以下改进：

### 核心优化

1. **并行处理效率提升**
   - 使用 `asyncio` 实现异步并行处理，大幅提高数据采集和处理速度
   - 优化内存使用，支持处理更大规模的调研数据

2. **数据处理流程优化**
   - 增强对不同格式字幕的兼容性（SRT、VTT等）
   - 改进数据合并算法，减少重复处理
   - 增加数据缓存机制，避免重复请求

3. **错误处理与鲁棒性**
   - 增加全面的错误处理机制，提高脚本稳定性
   - 添加输入参数验证，避免无效输入导致的崩溃
   - 实现网络请求失败时的重试逻辑

4. **功能扩展**
   - 支持更多平台的内容采集（YouTube、播客平台等）
   - 增加多语言支持，优化非英语人物的蒸馏效果
   - 提供更详细的质量检查报告

5. **用户体验改进**
   - 提供更详细的命令行参数说明
   - 增加进度显示和状态反馈
   - 生成更清晰的报告和摘要

## 安装

```bash
# 克隆仓库
git clone https://github.com/xiaojc9527/nuwa-skill.git
cd nuwa-skill

# 安装依赖
pip install -r requirements.txt

# 安装为Claude Code技能
npx skills add xiaojc9527/nuwa-skill
```

## 使用方法

### 基本用法

1. **蒸馏人物思维**
   ```
   > 蒸馏一个保罗·格雷厄姆
   > 造一个张小龙的视角Skill
   > 帮我做一个段永平的Skill
   ```

2. **调用生成的Skill**
   ```
   > 用芒格的视角帮我分析这个投资决策
   > 费曼会怎么解释量子计算？
   > 切换到Naval，我在纠结三件事
   ```

### 工具脚本使用

1. **下载字幕**
   ```bash
   # 从YouTube视频下载字幕
   ./scripts/download_subtitles.sh <YouTube_URL> [输出目录]
   ```

2. **合并调研结果**
   ```bash
   # 合并多个Agent的调研结果
   python3 scripts/merge_research.py --output research_summary.csv
   ```

3. **质量检查**
   ```bash
   # 检查SKILL.md的质量
   python3 scripts/quality_check.py SKILL.md --output quality_report.md
   ```

4. **字幕转转录**
   ```bash
   # 将字幕文件转换为纯文本转录
   python3 scripts/srt_to_transcript.py <subtitle_file> --output <transcript_file>
   ```

## 工作原理

输入一个名字后，女娲做四件事：

1. **六路并行采集** ——著作、播客/访谈、社交媒体、批评者视角、决策记录、人生时间线，6个Agent同时跑，各自存档。

2. **三重验证提炼** ——一个观点要被收录为心智模型，必须：跨2+个领域出现过（不是随口一说）、能推断对新问题的立场（有预测力）、不是所有聪明人都会这么想（有排他性）。三个都过才收录。

3. **构建Skill** ——3-7个心智模型 + 5-10条决策启发式 + 表达DNA + 价值观与反模式 + 诚实边界，写入SKILL.md。

4. **质量验证** ——拿3个此人公开回答过的问题测试，方向一致才通过。再用1个他没讨论过的问题测试，Skill应该表现出适度不确定而非斩钉截铁。

## 已蒸馏人物

女娲已蒸馏了13位人物 + 1个主题。每个都是独立的、可直接安装使用的Skill：

### 人物Skill

| 人物 | 领域 | 独立仓库 | 一键安装 |
|------|------|----------|----------|
| Paul Graham | 创业/写作/产品/人生哲学 | paul-graham-skill | `npx skills add alchaincyf/paul-graham-skill` |
| 张一鸣 | 产品/组织/全球化/人才 | zhang-yiming-skill | `npx skills add alchaincyf/zhang-yiming-skill` |
| Karpathy | AI/工程/教育/开源 | karpathy-skill | `npx skills add alchaincyf/karpathy-skill` |
| Ilya Sutskever | AI/研究/深度学习 | ilya-sutskever-skill | `npx skills add alchaincyf/ilya-sutskever-skill` |
| MrBeast | 内容创作/YouTube/商业 | mrbeast-skill | `npx skills add alchaincyf/mrbeast-skill` |
| Trump | 政治/沟通/品牌 | trump-skill | `npx skills add alchaincyf/trump-skill` |
| Steve Jobs | 产品/设计/领导力 | steve-jobs-skill | `npx skills add alchaincyf/steve-jobs-skill` |
| Elon Musk | 科技/创业/领导力 | elon-musk-skill | `npx skills add alchaincyf/elon-musk-skill` |
| Munger | 投资/人生哲学/思维模型 | munger-skill | `npx skills add alchaincyf/munger-skill` |
| Feynman | 物理/教育/沟通 | feynman-skill | `npx skills add alchaincyf/feynman-skill` |
| Naval | 创业/投资/人生哲学 | naval-skill | `npx skills add alchaincyf/naval-skill` |
| Taleb | 风险管理/哲学/随机性 | taleb-skill | `npx skills add alchaincyf/taleb-skill` |
| 张雪峰 | 教育/职业规划/考研 | zhangxuefeng-skill | `npx skills add alchaincyf/zhangxuefeng-skill` |

### 主题Skill

| 主题 | 描述 | 独立仓库 | 一键安装 |
|------|------|----------|----------|
| X导师 | 人生与职业发展导师 | x-mentor-skill | `npx skills add alchaincyf/x-mentor-skill` |

## 仓库结构

```
uwa-skill/
├── scripts/            # 工具脚本
│   ├── download_subtitles.sh  # 下载字幕
│   ├── merge_research.py      # 合并调研结果
│   ├── quality_check.py       # 质量检查
│   └── srt_to_transcript.py   # 字幕转转录
├── examples/           # 示例
├── references/         # 参考资料
├── README.md           # 项目说明
└── LICENSE             # 许可证
```

## 诚实边界

每个Skill都明确标注做不到什么：

- **蒸馏不了直觉**——框架能提取，灵感不能
- **捕捉不了突变**——截止到调研时间的快照
- **公开表达 ≠ 真实想法**——只能基于公开信息

一个不告诉你局限在哪的Skill，不值得信任。

## 许可证

MIT — 随便用，随便改，随便造。

## 关于作者

优化版由 xiaojc9527 基于原始项目改进。

原始项目作者：花叔 Huashu — AI Native Coder，独立开发者，代表作：小猫补光灯（AppStore 付费榜 Top1）
