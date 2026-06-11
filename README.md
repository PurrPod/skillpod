# PurrCat Skills Ecosystem

欢迎来到 PurrCat 官方技能（Skill）扩展库！这里是 PurrCat Agent 生态的"应用商店"。我们收录了由官方维护的高质量技能，以及来自开源社区的优秀贡献。

---

## 1. 技能安装指南

在执行安装前，请确保本地已配置最新版本的 `purrcat` 命令行工具。
基于本仓库提供的全局注册表 (`registry.json`)，支持通过**技能短名**进行标准安装：

```bash
# 格式: purrcat install skill <技能短名>
purrcat install skill stem-note-skill
```

对于尚未收录至注册表的第三方技能，支持通过指定目标代码目录的完整 URL 进行在线安装：

```bash
purrcat install skill https://github.com/PurrPod/skills/tree/main/official/stem-note-skill
```

---

## 2. 仓库架构说明

本仓库具备双重属性：既是扩展技能的代码托管中心，也是 PurrCat CLI 依赖的**核心注册表（Registry）**。技能模块按维护主体划分为官方与社区两类：

```text
skills/
├── .github/workflows/   # CI/CD 自动化构建流水线配置
├── scripts/             # 注册表构建与校验脚本
├── external.json        # 外部第三方仓库技能的链接索引清单
├── registry.json        # 全局注册表 (由 GitHub Actions 自动生成，请勿手动修改)
├── README.md            # 本说明文档 (由 GitHub Actions 自动更新)
│
├── official/            # 官方核心技能（由 PurrCat 核心团队维护，保证长期稳定性）
│   ├── stem-note-skill/    
│   └── ...
│
└── community/           # 社区扩展技能（由开源社区开发者提供与维护）
    ├── web-scraper/       
    └── ...

```

---

## 3. 已收录技能清单

以下列表展示当前注册表中已收录的技能。*(注：本列表由自动化流水线实时生成)*

### Official (官方核心)

<!-- BEGIN_OFFICIAL_TABLE -->
| 技能短名 (Install ID) | 技能名称 | 描述 | 作者 |
| :--- | :--- | :--- | :--- |
| **`stem-note-skill`** | [stem-note-skill](https://github.com/PurrPod/skillpod/tree/main/official/stem-note-skill) | 处理计算机科学（CS）及泛理工科（数学、物理、EE等）资料复习。提供硬性考点覆盖、跨学科题库生成，并自动化编译包含总导航目录(index)的全书级沉浸式分屏交互 HTML。 | PurrCat Official |

<!-- END_OFFICIAL_TABLE -->

### Community (社区扩展)

<!-- BEGIN_COMMUNITY_TABLE -->
| 技能短名 (Install ID) | 技能名称 | 描述 | 作者 |
| :--- | :--- | :--- | :--- |
| **`example-skill`** | [example-skill](https://github.com/PurrPod/skillpod/tree/main/community/example-skill) | 社区技能示例模板，展示如何编写一个 PurrCat Skill。 | Community Contributor |
| **`web-scraper`** | [Web Scraper](https://github.com/Alice/my-purr-skills/tree/main/web-scraper) | 强大的网页抓取与解析技能。 | Alice |

<!-- END_COMMUNITY_TABLE -->

---

## 4. 贡献指南

本仓库实行**全自动化**的注册表管理机制。贡献者仅需关注业务代码与 `SKILL.md` 元数据的编写，注册表的合并与发布由 CI 流水线自动完成。

### 方式一：将代码托管至本仓库（推荐）

1. **分支管理**：Fork 本仓库，并基于最新主干代码创建特性分支。
2. **创建目录**：在 `community/` 目录下创建独立的技能文件夹（例如：`community/data-analyzer/`），并将相关代码与脚本置于其中。
3. **配置元数据 (严格要求)**：

必须在技能文件夹内提供 `SKILL.md` 文件，包含标准的 YAML frontmatter。**`name` 字段必须与所在文件夹的名称严格一致**。示例：
```yaml
---
name: data-analyzer
description: 提供结构化数据清洗与分析能力。
author: DeveloperName
tags: [data, analysis]
license: MIT
---

```


4. **提交代码 (PR)**：
* **CI 合规性校验**：若文件夹名称与 `name` 字段不匹配，流水线将阻断合并请求。
* **自动化发布**：请勿在提交中包含对 `registry.json` 或 `README.md` 的手动修改。PR 审核通过并合并后，流水线将自动扫描 `SKILL.md`，更新全局注册表并重写本文档的技能清单。



### 方式二：收录外部仓库技能

若技能代码已托管于独立的外部仓库，可将其以索引的形式收录至本市集：

1. 编辑根目录下的 `external.json` 文件。
2. 以技能短名为键值（Key），按既有格式补充元数据，并确保 `source_url` 指向确切的技能目录。
3. 提交 Pull Request，通过后流水线将自动将其合并至全局注册表中。

---

## 5. 开源协议 (License)

* **仓库基础设施**：本仓库的目录结构、构建脚本及相关说明文档均遵循 MIT 协议。
* **独立技能协议**：**本仓库中收录的各级技能均独立适用其自身的开源协议。** 在安装或使用特定技能前，请务必查阅该技能目录下的 `LICENSE` 文件或 `SKILL.md` 中的授权说明。若未提供独立的协议声明，则默认继承本仓库的 MIT 协议。
