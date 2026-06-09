# 测试用例数据契约

`test-cases.json` 是自动化测试阶段的单一事实源，既给人 review，也给机器生成执行脚本。

`test-cases.sh` 必须从 `test-cases.json` 生成。不要再额外维护一份 Markdown 用例，也不要在 Shell 中手写用例。

## 已确认的 CLI 能力

### Web: `@zegocloud/auto-web`

根据 `/Users/oliver/code/zegocloud-auto-web` 源码和本地 help 确认：

| 命令 | 关键参数 | 说明 |
|------|----------|------|
| `connect` | `--url`, `--tab` | 创建或切换命名标签页 |
| `act` | `--prompt`, `--tab` | 执行自然语言动作和验证 |
| `take_screenshot` | `--tab` | 当前标签页截图 |
| `disconnect` | 无 | 清理标签页状态，浏览器进程保留 |
| `list_tabs` / `list-tabs` | 无 | 查看标签页 |
| `report-tool` | `--action`, `--htmlPath`, `--outputDir` | 转换 Midscene 报告 |

`@zegocloud/auto-web` 当前没有 `assert` 命令，所以 Web 用例必须把动作和预期都写入同一个 `act --prompt`。

### Android: `@midscene/android@1`

本地 help 确认：

| 命令 | 关键参数 | 说明 |
|------|----------|------|
| `connect` | `--device-id` / `--deviceId`, `--use-scrcpy` / `--useScrcpy` | 连接 Android 设备 |
| `act` | `--prompt`, `--device-id` / `--deviceId`, `--use-scrcpy` / `--useScrcpy` | 执行动作 |
| `assert` | `--prompt`, `--image`, `--imageName`, `--device-id` / `--deviceId` | 自然语言断言 |
| `take_screenshot` | `--device-id` / `--deviceId`, `--use-scrcpy` / `--useScrcpy` | 截图 |
| `disconnect` | 无 | 断开设备连接 |

### iOS: `@midscene/ios@1`

本地 help 确认：

| 命令 | 关键参数 | 说明 |
|------|----------|------|
| `connect` | `--device-id` / `--deviceId`, `--wda-host`, `--wda-port`, `--session-id`, `--use-w-d-a`, `--wda-mjpeg-port` | 连接 iOS 设备或模拟器 |
| `act` | 同 `connect` 参数 + `--prompt` | 执行动作 |
| `assert` | 同 `connect` 参数 + `--prompt`, `--image`, `--imageName` | 自然语言断言 |
| `take_screenshot` | 同 `connect` 参数 | 截图 |
| `disconnect` | 无 | 断开 WDA 连接 |

## 文件位置

```text
doc-test-reports/{run-name}/auto-test/
  test-cases.json
  test-cases.sh
```

## JSON 结构

```json
{
  "schemaVersion": "auto-test-demo/v1",
  "meta": {
    "product": "AIAgent",
    "platform": "web",
    "scope": "quick-start",
    "runName": "aiagent-web-quick-start-2026-06-08",
    "demoName": "aiagent-web-quick-start-demo",
    "projectDir": "doc-test-reports/aiagent-web-quick-start-2026-06-08/examples/aiagent-web-quick-start-demo",
    "reportDir": "doc-test-reports/aiagent-web-quick-start-2026-06-08/auto-test"
  },
  "runtime": {
    "platform": "web",
    "baseUrl": "http://localhost:5173",
    "env": {
      "MIDSCENE_REPLANNING_CYCLE_LIMIT": "15"
    },
    "setupCommands": [
      "npm install",
      "npm run dev -- --host 127.0.0.1 > \"$REPORT_DIR/logs/dev-server.log\" 2>&1 & echo $! > \"$REPORT_DIR/logs/dev-server.pid\"",
      "sleep 5"
    ],
    "preConnectCommands": [
      "npx -y @zegocloud/auto-web disconnect 2>/dev/null || true"
    ],
    "teardownCommands": [
      "npx -y @zegocloud/auto-web disconnect 2>/dev/null || true",
      "if [ -f \"$REPORT_DIR/logs/dev-server.pid\" ]; then kill \"$(cat \"$REPORT_DIR/logs/dev-server.pid\")\" 2>/dev/null || true; fi"
    ]
  },
  "targets": [
    {
      "id": "alice",
      "label": "Alice",
      "type": "web-tab",
      "tab": "alice",
      "url": "http://localhost:5173"
    }
  ],
  "cases": [
    {
      "id": "TC-001",
      "title": "登录 - Alice",
      "target": "alice",
      "dependent": null,
      "precondition": "无",
      "action": "在用户 ID 输入框输入 user_alice，点击登录按钮",
      "expected": "页面进入主界面，且没有报错信息",
      "waitAfterSec": 1,
      "screenshot": "TC-001-login-alice.png"
    }
  ]
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `schemaVersion` | 是 | 固定为 `auto-test-demo/v1` |
| `meta.runName` | 是 | `{product}-{platform}-{scope}-{date}` |
| `meta.projectDir` | 是 | 示例项目目录，通常是 `doc-test-reports/{run-name}/examples/{demo-name}` |
| `meta.reportDir` | 是 | 自动化测试报告目录 |
| `runtime.platform` | 是 | `web` / `android` / `ios` / `desktop` / `harmonyos` |
| `runtime.env` | 否 | 写入 Shell 的环境变量 |
| `runtime.setupCommands` | 否 | 连接设备或打开页面前执行。agent 可在这里补充安装、启动服务、安装 APK 等逻辑 |
| `runtime.preConnectCommands` | 否 | 连接测试目标前执行，常用于清理旧会话 |
| `runtime.teardownCommands` | 否 | 测试结束后执行，必须尽量释放服务、浏览器、设备连接 |
| `targets[].id` | 是 | 用例引用的目标 ID |
| `targets[].type` | 是 | `web-tab` / `android-device` / `ios-device` / `desktop-session` / `harmony-device` |
| `targets[].tab` | Web 必填 | `@zegocloud/auto-web --tab` |
| `targets[].url` | Web 必填 | `@zegocloud/auto-web connect --url` |
| `targets[].deviceId` | Android/iOS/HarmonyOS 建议填写 | 对应设备 ID 或 UDID |
| `cases[].id` | 是 | `TC-001` 格式，必须唯一 |
| `cases[].target` | 是 | 指向 `targets[].id` |
| `cases[].dependent` | 是 | 依赖的前置用例 ID；无依赖写 `null`；如果确实依赖多个前置用例，可写数组，如 `["TC-001","TC-002"]` |
| `cases[].precondition` | 是 | 人可 review 的前提条件；无前提写 `无` |
| `cases[].action` | 是 | 人可 review 的操作步骤 |
| `cases[].expected` | 是 | 人可 review 的预期结果 |
| `cases[].waitAfterSec` | 否 | 用例执行后等待秒数 |
| `cases[].screenshot` | 否 | 截图文件名；不填则由生成器按 ID 生成 |

## Prompt 生成规则

不要在 JSON 中维护单独的 `prompt` 字段。生成器会根据三段内容拼出实际 `act --prompt`：

```text
如果 precondition 不是“无”：
先确认前提条件：{precondition}。如果前提条件不满足，直接报告失败并说明当前界面状态；不要继续执行后续操作。前提条件满足后，执行操作：{action}。然后确认预期结果：{expected}。

如果 precondition 是“无”：
执行操作：{action}。然后确认预期结果：{expected}。
```

## 对齐要求

1. `test-cases.sh` 必须从 `test-cases.json` 生成，不手写用例循环。
2. agent 只能修改 `test-cases.json` 中的用例字段，或修改 `runtime.*Commands` 处理环境准备和收尾。
3. 如果人工 review 后修改了用例，必须改 `test-cases.json`，再重新生成 Shell。
4. 禁止在 `test-cases.sh` 中新增和 `test-cases.json` 不存在的测试用例。
5. 禁止用 `grep` 匹配自然语言输出判断通过。通过/失败由 `act` 的 exit code 决定。

## 依赖跳过策略

每个用例都必须填写 `dependent`，用来表达测试流程中的前置依赖关系。

执行规则：

1. 无依赖用例写 `"dependent": null`。
2. 依赖一个前置用例时写该用例 ID，例如 `"dependent": "TC-001"`。
3. 依赖多个前置用例时可写数组，例如 `"dependent": ["TC-001", "TC-002"]`。
4. `dependent` 只能引用更早定义的用例，不能引用自己或后面的用例。
5. 生成脚本会按 JSON 顺序执行用例；执行当前用例前先检查依赖用例状态。
6. 只有所有依赖用例状态都是 `passed`，当前用例才会执行。
7. 任一依赖用例 `failed` 或 `skipped` 时，当前用例写入 `test-results.jsonl`，状态为 `skipped`，message 为 `skipped because dependent case ... did not pass`。
8. 因此设计用例时必须显式建立依赖链。例如：登录 `TC-001` → 创建社群 `TC-002` → 创建频道 `TC-003` → 发送消息 `TC-004`。
