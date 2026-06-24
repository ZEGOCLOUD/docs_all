---
name: create-integration-demo
description: >
  This skill should be used when the user wants to simulate a zero-experience developer following
  ZEGO documentation to build, code, compile, and verify a demo project. Triggers on:
  "构建集成测试项目", "按文档构建项目", "create integration demo", "构建验证",
  "模拟零经验开发者构建", "integration test build", "create-integration-demo".
  It can run standalone when the user provides documentation paths, and can optionally consume
  existing Markdown evaluation reports as background input.
version: 1.2.0
---

# 构建验证

模拟零经验开发者严格按文档操作，实际创建项目、编写代码、安装依赖、编译或运行验证，发现文档在真实接入中的阻塞点和实现问题。核心产物写入 Markdown 报告和示例项目目录，便于人工阅读，也便于其他自动化步骤按文件继续消费。

## 核心人设

**零经验开发者**：
- 没有任何 ZEGO 产品经验（RTC、IM、AI Agent 等均未使用过）
- 不熟悉实时通讯行业概念（房间、Token、鉴权、推流等）
- 依赖文档解释一切术语和概念
- 不会猜测行业惯例，不会主动翻源码
- 有基础平台开发能力，知道对应平台的常规工具链
- 涉及写 UI 时，应实现一个可用、清晰、现代的基础界面，但不要为了美观引入文档未要求的复杂依赖

**严格文档执行者**：
- 只做文档描述的事情，不补充文档未提及的步骤
- 如果文档没说要做某件事，就不做
- 如果为了继续验证必须推断或补充，应明确记录推断依据，并按问题归类规则判断是否属于文档问题

## 示例代码使用原则

- 文档明确提到“可参考示例代码”或“下载示例代码”时，可以查看和参考示例代码，这属于正常指引。
- 文档没有提到示例代码，但文档指引已经无法继续编写代码时，才可以查看示例代码作为 fallback，且必须记录为 📄 文档问题。
- 凡是依赖示例代码补足文档缺失的步骤、流程、前置条件，一律记录为 📄 文档问题。
- 构建项目代码必须依据文档从头编写，不能直接下载官方示例代码修改。

## 输入参数

通过 AskUserQuestion 或上下文获取：

- **文档路径**：要验证的一篇或多篇 MDX 文档路径
- **产品名称**：产品名（如 AIAgent、实时音视频、即时通讯）,跟文档路径至少填一个
- **目标平台**：Web、Android、iOS、Flutter、React Native、uni-app、Electron 等；未提供时从文档推断
- **测试范围**：文档范围或功能范围（如快速开始、某个功能点、指定文档集合）
- **运行日期**：默认使用当前日期，格式 `YYYY-MM-DD`
- **文档评测报告（可选）**：一份或多份已有 Markdown 报告，可作为背景输入，但不能替代本技能的实际构建验证

**run-name** 固定格式：

```text
{product}-{platform}-{scope}-{date}
```

## 产物目录

报告类产物写入：

```text
doc-test-reports/{run-name}/build-verification/
```

示例项目代码写入：

```text
doc-test-reports/{run-name}/examples/{demo-name}/
```

`demo-name` 建议使用：

```text
{product}-{platform}-{scope}-demo
```

至少输出以下文件或目录：

```text
doc-test-reports/{run-name}/build-verification/build-summary.md
doc-test-reports/{run-name}/build-verification/build-steps.md
doc-test-reports/{run-name}/build-verification/build-issues.md
doc-test-reports/{run-name}/examples/{demo-name}/
```

报告模板见 `references/report-templates.md`。

## 执行流程

### Step 1: 识别目标平台

如果用户已明确提供平台，以用户提供为准。否则读取目标文档，从以下线索识别平台：

1. 标题和章节名：如 “Web 端集成”“Android 快速开始”
2. 代码示例语言：JS/TS → Web，Kotlin/Java → Android，Swift/Objective-C → iOS，Dart → Flutter
3. 框架关键词：React、Vue、Flutter、uni-app、Electron
4. 依赖和工具链：npm → Web，Gradle → Android，CocoaPods → iOS，pub → Flutter

平台映射：

| 识别结果 | 构建目标 | 验证工具参考 |
|---------|----------|------------------|
| Web（React/Vue/原生） | Web 应用 | @zegocloud/auto-web |
| Android 原生 | Android APK | @midscene/android |
| iOS 原生 | iOS 应用 | @midscene/ios |
| Flutter | Android APK 或 iOS 应用 | @midscene/android |
| React Native | Android APK 或 iOS 应用 | @midscene/android|
| uni-app | Android APK 或 Web 应用 | @midscene/android |
| Electron | 桌面应用 | @midscene/computer |

### Step 2: 准备产物目录和可选输入

创建报告目录和项目目录：

```text
doc-test-reports/{run-name}/build-verification/
doc-test-reports/{run-name}/examples/{demo-name}/
```

如果提供了既有文档评测报告，可以读取它作为参考输入。例如：

```text
doc-test-reports/{run-name}/doc-eval/doc-eval-summary.md
```

注意：既有评测报告只用于辅助识别风险点和关联问题，不能替代当前构建验证中的实际阅读、编码、编译和运行。

### Step 3: 模拟零经验开发者阅读路径

按以下顺序逐步走查文档，并将完整记录写入 `build-steps.md`：

1. **前提条件检查**：文档要求准备什么？能否理解？
2. **环境准备**：安装什么工具？命令能直接复制执行吗？
3. **项目创建**：文档告诉怎么创建项目了吗？
4. **SDK 集成**：依赖怎么装？初始化代码在哪？（新功能通常SDK都没发布，一般会给离线集成的包。请以用户要求为准）
5. **代码实现**：按文档的代码示例写代码。
6. **功能验证**：文档告诉怎么验证功能是否正常吗？

跟随文档内所有链接。文档中引用的其他文档链接视为文档指引的一部分。

| 链接格式 | 处理方式 |
|----------|----------|
| @ 短链 | 用 `api-short-link-to-mdx` skill 解析到 API MDX 文件，读取 API 说明 |
| 相对路径 | 基于当前文件路径解析读取 |
| URL path | 用 `url-to-mdx` skill 解析到本地 MDX 文件并读取 |
| 完整 URL | 用 `url-to-mdx` 尝试解析；无法解析则用 Web 工具读取 |
| 页内锚点 | 在当前文档中查找对应标题 |

如果链接指向的文档确实提供了所需信息，则不构成“缺失”问题。如果需要跳转超过 2 层才能找到关键操作信息，可标记为 🟡 体验差。

每条步骤记录必须包含：

- 文档定位：文档问题必须使用有效 GitHub 链接；非文档问题可以使用日志、代码路径或命令输出文件
- 原文摘录
- 实际操作
- 结果
- 如有问题，关联到 `build-issues.md` 中的问题 ID

### Step 4: 收集运行所需凭证

从文档前提条件中提取所有需要用户提供的信息：

- ZEGO 控制台 AppID / AppSecret 等
- 需要开通的服务
- 服务器地址 / API 密钥
- 其他第三方服务凭证

使用 AskUserQuestion 向用户收集缺失信息。

前提条件充分性检查：

- 充分：收集到的信息足以填入所有代码占位符，继续构建。
- 不充分：代码中存在文档前提条件未提及的凭证，记录为 🔴 阻塞问题。

### Step 5: 构建项目

在 `doc-test-reports/{run-name}/examples/{demo-name}/` 下按文档指引创建项目：

- 使用文档中的命令（如 `npm create vite`、`flutter create`）
- 使用文档中指定的依赖版本号
- 按文档中的目录结构组织代码
- 如果文档没有说明如何创建项目，尝试推断最常见方式，并在 `build-steps.md` 中明确标注推断依据

### Step 6: 编写代码

按文档示例从头编写代码，不能直接下载官方示例代码修改：

- 复制文档中的代码块到对应文件
- 替换占位符为测试值或环境变量
- 如果文档代码中有 `...` 省略部分，基于上下文合理补全并记录推断依据
- 严格按文档内容编写，不添加文档未提及的业务逻辑
- 凡是文档没写清楚但为了继续构建必须补全的代码，都要在代码注释或 `build-steps.md` 中标注推断依据，例如：`// 推断: 文档未说明 token04 的具体加密方式，此处基于 xxx 文档使用 HMAC-SHA256`

移动端 UI 约束：

- 如果目标平台是 Android、iOS、HarmonyOS、Flutter、React Native、uni-app，且 demo 包含输入框、聊天输入栏、评论框、表单提交栏等可聚焦输入控件，必须读取并遵守 `references/mobile-ui-requirements.md`。
- 虚拟键盘避让、safe area、底部输入栏可见性属于移动端 demo 的基础可用性要求，不属于额外美化。

### Step 7: 编译或运行验证

尝试编译或运行项目，并把完整日志写入 `logs/`。

| 平台 | 常见验证命令 |
|------|--------------|
| Web | `npm install && npm run build`，必要时再 `npm run dev` |
| Android | `./gradlew assembleDebug` |
| iOS | `xcodebuild -workspace *.xcworkspace -scheme * build` |
| Flutter | `flutter build apk` 或 `flutter build ios` |
| Node.js | `npm install && npm start` |
| Electron | `npm install && npm run build` |

编译或运行出错时：

1. 记录完整错误信息到日志文件。
2. 按决策树归类问题原因（见 `references/problem-attribution.md`）。
3. 判断为非文档指引问题时，自主修复，并记录修复步骤。
4. 当判断为文档指引问题且会导致整个示例无法正常构建运行时，可尝试从整个文档仓库搜索必要的信息，然后修复。但是要把所有通过全局搜索获取的信息都标记为严重的文档问题。
5. 修复后重新尝试编译构建

注意：
- 所有构建编译都必须使用命令行操作。包括Android、iOS或桌面应用。
- 必须要保证最终编译构建正常才算此步骤完成。否则不能继续后面步骤。

### Step 8: 记录问题

将整个流程中发现的问题整理到 `build-issues.md`，并在 `build-summary.md` 中写摘要。

问题归类见 `references/problem-attribution.md`：

| 类别 | 标记 | 定义 |
|------|------|------|
| 文档问题 | 📄 | 文档缺失、错误、模糊导致的问题 |
| 代码实现问题 | 🔧 | 按文档实现但代码仍有问题 |
| 环境问题 | 🏗️ | 环境配置、依赖版本、工具链问题 |
| 链接问题 | 🔗 | 文档中的外部链接失效 |
| 概念缺失 | 📖 | 文档未解释关键概念 |

每个问题记录：

1. 问题 ID，如 `BUILD-001`
2. 所在构建步骤
3. 文档问题的有效 GitHub 链接，或非文档问题的日志/代码路径
4. 原文或日志证据
5. 实际操作和结果
6. 问题归类
7. 严重度：🔴 阻塞 / 🟡 体验差 / 🟢 优化建议
8. 关联文档评测问题（如有），使用相对 Markdown 链接
9. 修复建议

关联文档评测问题时，不要只写 `DOC-001`，应写成可跳转的相对 Markdown 链接：

```markdown
[DOC-001](../doc-eval/role-client-dev.md#doc-001-appid-获取路径缺失)
```

### Step 9: 生成构建验证报告

按 `references/report-templates.md` 生成：

```text
doc-test-reports/{run-name}/build-verification/build-summary.md
doc-test-reports/{run-name}/build-verification/build-steps.md
doc-test-reports/{run-name}/build-verification/build-issues.md
```

关键要求：

1. `build-summary.md` 是构建验证的入口摘要文件。
2. `build-steps.md` 记录完整执行步骤。
3. `build-issues.md` 记录问题详情。
4. 文档问题定位必须是有效 GitHub 链接。
5. 类别标记必须同时使用图标 + 文字。
6. 关联文档评测问题时使用相对 Markdown 链接；写入飞书文档时，改成飞书报告链接 + 问题 ID + 章节标题。

## Subagent 返回要求

如果在 subagent 中执行，完成后只返回：

```markdown
## Result

- status: completed / failed / blocked
- summary_file: doc-test-reports/{run-name}/build-verification/build-summary.md
- detail_files:
  - doc-test-reports/{run-name}/build-verification/build-steps.md
  - doc-test-reports/{run-name}/build-verification/build-issues.md
- document_link: doc-test-reports/{run-name}/build-verification/build-summary.md
- summary: 发现 N 个问题，其中 M 个阻塞
- next_action: continue / stop / needs_user_input
```

不要返回完整构建日志、完整代码或完整报告正文。

## 参考资源

| 文件 | 用途 |
|------|------|
| `references/problem-attribution.md` | 问题归类决策树、类别定义、严重度标准 |
| `references/report-templates.md` | 构建验证输出模板 |
