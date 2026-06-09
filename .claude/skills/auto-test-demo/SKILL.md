---
name: auto-test-demo
description: >
  This skill should be used when the user wants to test a demo project — designing test cases,
  executing automated tests, taking screenshots, and packaging the project. Also handles creating
  test-cases.json and test-cases.sh for example code projects. Triggers on: "test demo", "run tests",
  "test the project", "验证功能", "测试 demo", "run test cases", "截图打包", "create test cases",
  "write test cases", "generate test cases", "design test cases for the demo", "create test-cases.json",
  "create test-cases.sh". Applicable to document example demos, access test demos, and competitive test demos.
version: 1.1.0
---

# Demo 项目自动化测试

对已构建的 demo 项目执行完整测试流程：分析代码 → 设计测试用例数据 → 生成可执行脚本 → 执行测试（含截图）。适用于接入测试、竞品测试 demo、文档示例代码等任何需要验证功能的场景。

`test-cases.json` 是测试用例的单一事实源，既给人 review，也给机器生成执行脚本。`test-cases.sh` 必须从同一个 JSON 生成。

## 前置条件

- 项目已构建完成，代码已写入 `doc-test-reports/{run-name}/examples/{demo-name}/` 目录
- 已识别目标平台（Web / Android / iOS / Flutter / Desktop / HarmonyOS）
- 项目已能通过编译验证
- 已确定报告目录：`doc-test-reports/{run-name}/auto-test/`

## 核心原则

### 1. 只测核心功能

Demo 项目不是生产软件，测试用例只覆盖 **核心 happy-path 流程**，验证 SDK 核心能力端到端可用。跳过：空输入验证、重复项防护、导航边界、国际化、数据持久化。

典型测试用例数量：每个功能项对应 1～2个用例。能确保核心功能点和流程按正常逻辑操作都覆盖即可。

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

### 5. 测试用例单一事实源

- 先写 `doc-test-reports/{run-name}/auto-test/test-cases.json`。
- 再用 `scripts/generate-test-artifacts.js` 生成 `test-cases.sh`。
- 人工 review 的对象是 `test-cases.json`；如果要改用例，直接改 JSON 并重新生成脚本。
- 禁止在 `test-cases.sh` 中手工新增、删除或改写测试用例。
- `test-cases.sh` 只允许在生成后的 hook 区域补充当前项目需要的环境变量、启动服务、安装 APK、清理设备、收尾逻辑。
- 测试通过/失败只看 `act` 的 exit code，禁止用 `grep` 匹配自然语言输出判断通过。
- 每个用例必须声明 `dependent`。无依赖写 `null`；依赖某个前置用例时写该用例 ID。依赖用例未通过时，当前用例自动标记为 `skipped`。

## 执行流程

### Step 1: 分析项目代码

先读取 `references/platform-mapping.md`，用其中的平台识别规则、编译命令、启动命令和截图方式判断当前项目的测试平台与运行入口。

读取并理解 demo 项目的核心功能：

1. 读取 `{example_dir}/interaction-design.md`（如有）了解交互流程
2. 读取 `{example_dir}/src` 下主要源文件理解实际实现
3. 识别 **核心功能**：demo 展示的关键能力
4. 确定 **用户角色**：（单用户 vs 多用户交互）
5. 确认 **平台**（Web / Android / iOS / Desktop / HarmonyOS）

### Step 2: 设计测试用例

如需要参考一个完整多用户用例结构，可读取 `examples/sample-test-cases.md`。该示例只用于理解 JSON 结构和用例拆分粒度，不要直接复制其中的产品、用户或文案。

测试用例设计的目标是把真实用户核心路径拆成可以被机器逐条执行、也能被人直接 review 的结构化数据。每个用例只保留四段核心语义：`dependent`、`precondition`、`action`、`expected`。

设计规则：

- **只覆盖核心 happy-path**：Demo 项目只验证 SDK 核心能力端到端可用，不扩展成生产级边界测试。
- **按真实用户顺序排列**：例如登录 → 进入功能页 → 发起操作 → 对端观察 → 结果验证。
- **建立依赖关系**：每个用例都要根据真实流程填写 `dependent`。例如创建频道依赖登录，发送消息依赖创建频道。
- **一个用例只做一个明确动作**：大的流程拆成多个有顺序依赖的最小步骤。比如“输入自己用户 ID 登录”是一个用例，“输入对方用户 ID 进入通话页”是下一个用例。
- **前提条件写当前可观察状态**：写“当前已在主界面且登录按钮显示已登录”，不要写“按钮从登录变成已登录”这种变化过程。
- **前提条件不满足即失败**：不继续执行 action，不尝试自行补救。
- **action 只写用户操作**：点击什么、输入什么、等待什么；不要混入预期结果。
- **expected 只写验证标准**：应该看到什么、听到什么、状态如何、是否无报错。
- **多用户场景成对设计**：发送方/操作方一个用例，接收方/观察方另一个用例，并用前提条件表达依赖关系。
- **依赖必须指向更早的用例**：`dependent` 只能引用前面已经定义的用例，不能引用自己或后面的用例。
- **明确 target**：每个用例必须指定在哪个浏览器标签页、设备或桌面会话上执行。
- **报错即失败**：expected 中必须包含“没有报错信息”或等价表述；如果 UI 上出现明确报错，该用例失败。

生成器会按以下规则拼出实际 `act --prompt`，不要在 JSON 里单独写 prompt：

```text
如果 precondition 不是“无”：
先确认前提条件：{precondition}。如果前提条件不满足，直接报告失败并说明当前界面状态；不要继续执行后续操作。前提条件满足后，执行操作：{action}。然后确认预期结果：{expected}。

如果 precondition 是“无”：
执行操作：{action}。然后确认预期结果：{expected}。
```

### Step 3: 生成 test-cases.json

写 JSON 前必须读取 `references/test-case-data.md`，按其中的数据契约填写 `meta`、`runtime`、`targets` 和 `cases`。平台命令参数不确定时，读取 `references/platform-command-reference.md`，不要凭记忆猜 CLI 参数。

写入：

```text
doc-test-reports/{run-name}/auto-test/test-cases.json
```

JSON 结构见 `references/test-case-data.md`。必须包含：

- `meta`: 产品、平台、范围、run-name、demo-name、项目目录、报告目录
- `runtime`: 平台、环境变量、setup/pre-connect/teardown 命令
- `targets`: 浏览器标签页、Android 设备、iOS 设备、桌面会话等测试目标
- `cases`: 真正的测试用例列表

`cases` 中每个用例必须同时写清楚：

- `id`: `TC-001` 格式
- `target`: 引用 `targets[].id`
- `dependent`: 依赖的前置用例 ID；无依赖写 `null`；多个依赖可写数组
- `precondition`: 人可 review 的前提条件
- `action`: 人可 review 的操作步骤
- `expected`: 人可 review 的预期结果
- `screenshot`: 该用例的截图文件名

### Step 4: 生成 test-cases.sh

使用 `scripts/generate-test-artifacts.js` 从 `test-cases.json` 生成：

```bash
node .claude/skills/auto-test-demo/scripts/generate-test-artifacts.js \
  doc-test-reports/{run-name}/auto-test/test-cases.json
```

生成产物：

```text
doc-test-reports/{run-name}/auto-test/test-cases.sh
```

生成后检查：

1. `test-cases.sh` 中的 `run_case` 调用数量与 `cases.length` 一致。
2. `test-cases.sh` 中没有额外手写测试用例。
3. `test-cases.sh` 可以包含环境准备和收尾逻辑，但只能来自 `runtime.setupCommands`、`runtime.preConnectCommands`、`runtime.teardownCommands` 或生成器预留 hook。


生成器会负责固定脚本骨架：

- `set +e` 和 `set -o pipefail`
- 创建 `logs/`、`screenshots/`
- 连接测试目标
- 按 JSON 顺序逐条执行用例
- 执行每个用例前检查 `dependent` 指向的前置用例状态；依赖未通过时，该用例记录为 `skipped`
- 每个用例执行后立即截图
- 将结果写入 `test-results.jsonl`
- 执行 teardown

agent 不需要手写这些固定逻辑。

### Step 5: 测试前准备

#### 通用处理
- 对于服务端、Web端应该重新编译和重启服务后再启动测试
- 对于iOS、Android、桌面端都应该重新安装应用后再启动测试

#### 平台相关处理

**Web 平台**：
- 自动化测试包已开启摄像头麦克风权限。无需再申请。
- 连接前必须先清理旧会话：`@zegocloud/auto-web` 基于 Puppeteer 启动 Chrome。如果上一次测试会话未正常关闭（进程崩溃、Ctrl+C 中断等），会残留 Chrome 僵尸进程，占用调试端口。新连接时 `Network.enable` 请求会发给旧进程，导致超时错误。所以必须在每次 `connect` 前先 `disconnect` 清理旧会话。如果 disconnect 后还是超时，可以尝试`pkill -f "chrome.*--remote-debugging-port" 2>/dev/null || true`

**Android 模拟器**:
- 每次新任务需要完全重启模拟器，否则因为之前测试任务遗留可能导致测试失败
- 如果遇到模拟器处于 offline 状态，直接关闭设备。如：`adb -s emulator-5554 emu kill`
- 尽可能复用现有的模拟器（~/Android/Sdk/emulator/emulator -list-avds）而不要自行创建，除非所有模拟器都无法启动或者异常
- 在重启或者关闭模拟器后必须重新启动保证模拟器在线并重新安装应用

### Step 6: 执行测试

确保应用已启动运行，或已在 `runtime.setupCommands` 中写好启动逻辑，然后执行测试脚本：

```bash
bash doc-test-reports/{run-name}/auto-test/test-cases.sh
```

执行完成后，检查：

```text
doc-test-reports/{run-name}/auto-test/test-results.jsonl
doc-test-reports/{run-name}/auto-test/logs/
doc-test-reports/{run-name}/auto-test/screenshots/
```

### Step 7: 生成测试报告

测试执行完成后，读取 `references/report-template.md`，按模板生成结构化报告。

**关键流程**：

1. **读取测试结果**：从 `test-results.jsonl` 提取每个用例的通过/失败状态
2. **收集截图**：从 `screenshots/` 收集每个用例的截图
3. **主动采集系统日志并分析失败用例**：
   - **测试框架不采集系统日志**（`@zegocloud/auto-web` 等 `@midscene/*` 工具只执行操作和截图，不采集 console/logcat）
   - 用例失败时，agent 必须自己主动采集系统日志：Web 用 Chrome DevTools MCP（`list_console_messages`）、Android 用 `adb logcat`、iOS 用 Xcode log
   - **采集时机**：每个用例失败后立即采集，不要等所有用例跑完再统一采集（日志可能已被覆盖）
   - **禁止仅凭截图表面现象推断原因**，必须结合主动采集到的系统日志分析
   - 如主动采集后日志为空，如实记录"主动采集 console，无任何输出，应用可能未正确初始化"
4. **生成报告**：按 `references/report-template.md` 写入 `doc-test-reports/{run-name}/auto-test/`

报告必须包含：
- 测试概览表格（总用例数、通过、失败、通过率）
- 用例结果表格（编号、名称、状态、截图文件名）
- 每个失败用例的详细分析（失败表现 + 系统日志 + 综合原因）
- 环境信息（OS、浏览器/运行时、SDK 版本、Node.js 版本）

### Step 8: 清理环境

测试完成后停止所有相关进程和设备，释放资源：

- **Web**: 停止本地服务器（如 Express、Vite dev server）、断开 auto-web 连接（`disconnect`）、终止 Chrome 进程（`pkill -f "zegocloud-auto-web"`)
- **Android**: 停止模拟器（`adb -s <device> emu kill`）或关闭真机上的 app
- **iOS**: 关闭模拟器（`xcrun simctl shutdown <udid>`）或终止 app 进程
- **Desktop**: 终止桌面应用进程
- **HarmonyOS**: 停止模拟器或关闭真机上的 app
