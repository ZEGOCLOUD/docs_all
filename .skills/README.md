# Claude Code Skills

这个目录包含项目特定的 Claude Code skills，用于增强团队的开发体验。

## 已安装的 Skills

### zh-translator
中文文档翻译 skill，支持：
- 基于 git commit 历史分析改动
- 生成翻译任务列表
- 使用术语表保持翻译一致性
- 支持多种产品线的术语对照

## 团队成员安装

运行安装脚本即可：

```bash
./.scripts/install_claude_skills.sh
```

脚本会：
1. 自动扫描 `.skills` 目录下的所有 skills
2. 在 `~/.claude/plugins/` 创建软链接
3. 列出所有已安装的 skills

## 添加新的 Skill

1. 在 `.skills` 目录下创建新的子目录
2. 在子目录中创建 `SKILL.md` 文件
3. 可选：添加 `scripts/`、`references/`、`assets/` 等资源目录
4. 运行安装脚本更新

## 目录结构

```
.skills/
├── README.md
└── zh-translator/
    ├── SKILL.md              # Skill 描述和工作流程
    ├── scripts/              # 可执行脚本
    │   └── analyze_changes.py
    └── references/           # 参考文档和术语表
        ├── common-terminology.csv
        └── products/
            ├── real_time_video_zh.csv
            ├── zim_zh.csv
            └── ...
```

## 使用 Skill

安装后，在 Claude Code 中直接使用即可，例如：

```
请帮我翻译从 commit abc123 到 HEAD 的改动
```

Skill 会自动加载并提供翻译功能。

## 更新 Skill

1. 更新 `.skills` 目录下的 skill 文件
2. 重新运行安装脚本

因为是软链接，更新会立即生效（无需重启 Claude Code）。
