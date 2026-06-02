---
name: auto-test-demo
description: >
  This skill should be used when the user wants to test a demo project — designing test cases,
  executing automated tests, taking screenshots, and packaging the project. Also handles creating
  test-cases.md and test-cases.sh for example code projects. Triggers on: "test demo", "run tests",
  "test the project", "验证功能", "测试 demo", "run test cases", "截图打包", "create test cases",
  "write test cases", "generate test cases", "design test cases for the demo", "create test-cases.md",
  "create test-cases.sh". Applicable to document example demos, access test demos, and competitive test demos.
version: 1.1.0
---

# Demo 项目自动化测试

对已构建的 demo 项目执行完整测试流程：分析代码 → 设计测试用例 → 生成自动化脚本 → 执行测试（含截图）。适用于接入测试、竞品测试 demo、文档示例代码等任何需要验证功能的场景。

## 前置条件

- 项目已构建完成，代码已写入 `examples/{项目名}/` 目录
- 已识别目标平台（Web / Android / iOS / Flutter / Desktop / HarmonyOS）
- 项目已能通过编译验证

## 核心原则

### 1. 只测核心功能

Demo 项目不是生产软件，测试用例只覆盖 **核心 happy-path 流程**，验证 SDK 核心能力端到端可用。跳过：空输入验证、重复项防护、登出/重登、错误消息验证、导航边界、国际化、数据持久化。

典型测试用例数量：5-10 个。超过 10 个说明过度测试。

### 2. 测试失败先查诊断输出，禁止凭症状猜原因

测试有用例失败时，必须先主动采集系统级诊断输出（浏览器 console、logcat、Xcode log 等），拿到错误信息后再分析根因。**测试框架不采集系统日志**，agent 必须自己用 Chrome DevTools MCP / `adb logcat` 等工具主动获取。禁止根据 UI 表面症状（黑屏、状态文字、空白页面）直接推断原因。

### 3. 测试用例必须符合真实用户流程（不可妥协）

**绝对不能为了测试通过而修改应用代码或降低测试预期。**

- 测试用例描述的是真实用户操作和真实预期结果
- 如果测试环境缺少某些条件（如无麦克风、无摄像头），测试失败是**正确结果**，说明应用在该环境下确实不可用
- **禁止**：修改应用代码绕过权限检查、降低预期结果、修改测试步骤来适应测试环境
- **禁止**：把 "用户应该看到登录成功" 改成 "用户应该看到某些日志"
- 测试失败 → 记录失败原因 → 如实报告，不做任何掩盖

### 4. 音视频画面的预期判断

模拟器或浏览器自动化测试中，音视频画面不可能呈现真实摄像头画面，应按以下标准判断：

| 现象 | 是否正常 | 说明 |
|------|---------|------|
| 花屏、雪花、彩色条纹、绿色/灰色填充 | ✅ 正常 | 模拟器/浏览器无真实摄像头，系统生成假画面 |
| 有画面在动（即使内容无意义） | ✅ 正常 | 说明视频流在传输，SDK 工作正常 |
| 纯黑无任何内容 | ❌ 不正常 | 视频流未建立或渲染失败 |
| 视频区域完全不存在（空白、占位符） | ❌ 不正常 | 视频组件未渲染或未挂载 |

**在测试用例和报告中**：预期结果应写"看到视频画面（花屏/雪花亦可）"而非"看到清晰画面"，但纯黑或无视频区域应判定为失败。

## 完整流程

### Step 1: 分析项目代码

读取并理解 demo 项目的核心功能：

1. 读取 `{example_dir}/interaction-design.md`（如有）了解交互流程
2. 读取 `{example_dir}/src` 下主要源文件理解实际实现
3. 识别 **核心功能** — 通常 3-5 个 demo 展示的关键能力
4. 确定 **用户角色**（单用户 vs 多用户交互）
5. 确认 **平台**（Web / Android / iOS / Desktop / HarmonyOS）

### Step 2: 设计测试用例

每个核心功能设计 **一个** happy-path 测试用例。规则：

- **多用户场景**：涉及交互的功能（聊天、通话、协作），设计配对用例——一个发送方/操作方，一个接收方/观察方
- **顺序流**：测试用例按自然用户流程排列（登录 → 操作 → 验证）
- **明确设备分配**：每个用例指定在哪个设备/标签页上执行
- **自然语言描述**：步骤描述精确、无歧义

### Step 3: 生成 test-cases.md

写入 `{example_dir}/test-cases.md`。**全部使用中文**（标题、表头、步骤描述、预期结果均为中文）。

```markdown
# 测试用例 - {项目名} ({平台})

> 平台: {平台} | 用户: {N} ({用户名}) | 仅覆盖核心功能

## 测试用例

| 编号 | 设备/标签 | 用例名称 | 操作步骤 | 预期结果 |
|------|----------|---------|---------|---------|
| TC-01 | 标签页: alice | 登录 - Alice | 在用户ID输入框输入 `user_alice`，点击登录按钮 | 页面跳转到主界面 |
| TC-02 | 标签页: bob | 登录 - Bob | 在用户ID输入框输入 `user_bob`，点击登录按钮 | 页面跳转到主界面 |
| TC-03 | 标签页: alice | 核心操作 | 操作步骤描述 | 预期看到的界面或状态 |
```

列定义：
- **编号**: TC-01, TC-02, ... 顺序编号
- **设备/标签**: 设备 ID 或浏览器标签名（如 `标签页: alice`, `设备: device_alice`）
- **用例名称**: 简短中文描述
- **操作步骤**: 精确的中文操作步骤
- **预期结果**: 操作后应看到的/确认的中文描述

### Step 4: 生成 test-cases.sh

写入 `{example_dir}/test-cases.sh`。根据平台选择对应模板（详见 `references/platform-*.md`）：

| 平台 | 包 | 连接命令 | 操作命令 |
|------|---|---------|---------|
| Web | `@zegocloud/auto-web` | `connect --url "$URL" --tab NAME` | `act --tab NAME --prompt "..."` |
| Android | `@midscene/android@1` | `connect --deviceId ID` | `act --device-id ID --prompt "..."` |
| iOS | `@midscene/ios@1` | `connect` | `act --prompt "..."` |
| Desktop | `@midscene/computer@1` | `connect` | `act --prompt "..."` |
| HarmonyOS | `@midscene/harmony@1` | `connect --deviceId ID` | `act --deviceId ID --prompt "..."` |

#### Web 平台浏览器权限

`@zegocloud/auto-web` 已内置媒体权限 flags（麦克风、摄像头、自动播放），无需额外配置。

#### Web 平台：连接前必须清理旧会话（重要）

`@zegocloud/auto-web` 基于 Puppeteer 启动 Chrome。如果上一次测试会话未正常关闭（进程崩溃、Ctrl+C 中断等），会残留 Chrome 僵尸进程，占用调试端口。新连接时 `Network.enable` 请求会发给旧进程，导致超时错误：

```
Error: Network.enable timed out
```

**必须在每次 `connect` 前先 `disconnect` 清理旧会话**：

```bash
# 连接前必须清理 — 防止僵尸 Chrome 导致超时
npx -y @zegocloud/auto-web disconnect 2>/dev/null || true

# 然后再连接
npx -y @zegocloud/auto-web connect --url "$URL" --tab alice
```

如果 `disconnect` 后仍然超时，说明有更早的僵尸进程，需要手动杀掉：

```bash
pkill -f "chrome.*--remote-debugging-port" 2>/dev/null || true
```

#### 脚本编写要点

- **一个 `act` 调用对应一个测试用例**
- **每个测试用例后立即截图**：用 `take_screenshot` 命令保存当前界面状态到 `midscene_run/screenshots/`，无论测试通过或失败都截图
- **描述性 prompt**：`--prompt` 文本必须完整自包含，包括做什么和确认什么
- **跨用户等待**：等待另一用户/设备接收时加 `sleep 3-5`
- **TOTAL_COUNT**：设为实际测试用例数量

#### 结果判断：必须用 exit code，不要 grep

**act 命令的退出码就是测试结果的可靠判断依据**：
- exit code 0 = 测试通过
- exit code 1 = 测试失败（输出含 `Error executing act: Task failed: ...`）

```
# 正确写法 — 用退出码判断
if npx -y @zegocloud/auto-web act --tab alice --prompt "..."; then
  echo "PASS: TC-01"
else
  echo "FAIL: TC-01"
  FAILED=$((FAILED + 1))
fi

# 错误写法 — grep 输出不可靠
npx -y @zegocloud/auto-web act --tab alice --prompt "..." 2>&1 | grep -qi "success"
```

不要用 `grep -qi` 匹配输出文字来判断成功或失败。原因：
1. 成功输出中没有通用的 "success" 关键词，只有 `Task finished, message: ...`
2. 某些场景 AI 执行了操作但结果不符预期，exit code 仍为 0 但实际失败——需要人工检查 report
3. grep 会误判边界情况

#### Prompt 编写规范

1. **自包含** — 包含所有上下文，不引用前面步骤
2. **动作 + 验证** — "Do X, then confirm Y is visible"
3. **具体化** — 使用界面中确切的元素标签、按钮文字、字段名
4. **单一职责** — 一个测试用例验证一个核心动作

示例：
```
"在消息输入框中输入'你好 Bob!'并按回车发送。确认该消息以绿色气泡的形式出现在右侧。"
```

#### 脚本骨架

```bash
#!/bin/bash
set +e
set -o pipefail

TOTAL_COUNT=N
FAILED=0
PASSED=0
SCREENSHOT_DIR="midscene_run/screenshots"

mkdir -p "$SCREENSHOT_DIR"

# 清理旧会话
npx -y @zegocloud/auto-web disconnect 2>/dev/null || true

# 连接
npx -y @zegocloud/auto-web connect --url "$URL" --tab alice

# TC-01
echo "执行 TC-01: 登录 - Alice"
if npx -y @zegocloud/auto-web act --tab alice --prompt "在用户ID输入框输入 user_alice，点击登录按钮。确认页面跳转到主界面。"; then
  echo "  通过: TC-01"
  PASSED=$((PASSED + 1))
else
  echo "  失败: TC-01"
  FAILED=$((FAILED + 1))
fi
npx -y @zegocloud/auto-web take_screenshot --tab alice 2>&1 | grep -o "Screenshot saved:.*" | awk '{print $NF}' | xargs -I{} cp {} "$SCREENSHOT_DIR/01-login-alice.png" 2>/dev/null || true

# ... 更多测试用例

echo ""
echo "========================================="
echo "测试结果: $PASSED/$TOTAL_COUNT 通过, $FAILED 失败"
echo "========================================="

npx -y @zegocloud/auto-web disconnect 2>/dev/null || true

if [ $FAILED -gt 0 ]; then
  exit 1
fi
```

注意：
- 脚本开头不要用 `set -e`，会导致失败时立即退出。用上述 if/else 模式逐条执行并计数。
- **必须用 `set -o pipefail`**，否则 `| tee` 管道会掩盖 npx 的真实退出码。
- **连接前先 `disconnect`** 清理旧会话，防止僵死浏览器导致超时。
- **每个用例后立即 `take_screenshot`**，无论通过或失败都截图。截图保存到 `screenshots/` 目录。

### Step 5: 执行测试

确保应用已启动运行，然后执行测试脚本：

```bash
cd examples/{项目名} && chmod +x test-cases.sh && bash test-cases.sh
```

执行完成后，检查 `midscene_run/screenshots/` 目录中的截图和 `midscene_run/` 中的报告。

### Step 6: 生成测试报告

测试执行完成后，生成结构化报告。模板见 `references/report-template.md`。

**关键流程**：

1. **读取测试结果**：从 `test-cases.sh` 的输出中提取每个用例的通过/失败状态
2. **收集截图**：从 `midscene_run/screenshots/` 收集每个用例的截图
3. **主动采集系统日志并分析失败用例**：
   - **测试框架不采集系统日志**（`@zegocloud/auto-web` 等 `@midscene/*` 工具只执行操作和截图，不采集 console/logcat）
   - 用例失败时，agent 必须自己主动采集系统日志：Web 用 Chrome DevTools MCP（`list_console_messages`）、Android 用 `adb logcat`、iOS 用 Xcode log
   - **采集时机**：每个用例失败后立即采集，不要等所有用例跑完再统一采集（日志可能已被覆盖）
   - **禁止仅凭截图表面现象推断原因**，必须结合主动采集到的系统日志分析
   - 如主动采集后日志为空，如实记录"主动采集 console，无任何输出，应用可能未正确初始化"
4. **生成报告**：按模板写入 `examples/{项目名}/test-report.md`

报告必须包含：
- 测试概览表格（总用例数、通过、失败、通过率）
- 用例结果表格（编号、名称、状态、截图文件名）
- 每个失败用例的详细分析（失败表现 + 系统日志 + 综合原因）
- 环境信息（OS、浏览器/运行时、SDK 版本、Node.js 版本）

### Step 7: 清理环境

测试完成后停止所有相关进程和设备，释放资源：

- **Web**: 停止本地服务器（如 Express、Vite dev server）、断开 auto-web 连接（`disconnect`）、终止 Chrome 进程（`pkill -f "zegocloud-auto-web"`)
- **Android**: 停止模拟器（`adb -s <device> emu kill`）或关闭真机上的 app
- **iOS**: 关闭模拟器（`xcrun simctl shutdown <udid>`）或终止 app 进程
- **Desktop**: 终止桌面应用进程
- **HarmonyOS**: 停止模拟器或关闭真机上的 app

## 参考资源

| 文件 | 用途 |
|------|------|
| `references/platform-mapping.md` | 平台识别规则、编译/启动/截图命令 |
| `references/platform-web.md` | Web 平台脚本模板（单用户 + 多标签） |
| `references/platform-android.md` | Android 平台脚本模板（单设备 + 多设备） |
| `references/platform-ios.md` | iOS 平台脚本模板（单设备） |
| `references/platform-desktop.md` | Desktop 平台脚本模板（单会话） |
| `references/platform-harmonyos.md` | HarmonyOS 平台脚本模板（单设备） |
| `references/report-template.md` | 测试报告模板（含失败分析格式） |
| `examples/sample-test-cases.md` | ZIM 聊天 demo 测试用例示例 |
