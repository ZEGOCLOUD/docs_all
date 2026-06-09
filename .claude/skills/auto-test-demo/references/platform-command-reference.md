# 平台命令参考

本文件只记录自动化测试工具的命令和参数。测试脚本骨架由 `scripts/generate-test-artifacts.js` 生成，不从本文件复制 shell 用例块。

## Web: `@zegocloud/auto-web`

来源：`/Users/oliver/code/zegocloud-auto-web` 源码与本地 `--help`。

| 操作 | 命令 |
|------|------|
| 连接标签页 | `npx -y @zegocloud/auto-web connect --url "$URL" --tab "$TAB"` |
| 执行动作和验证 | `npx -y @zegocloud/auto-web act --tab "$TAB" --prompt "$PROMPT"` |
| 截图 | `npx -y @zegocloud/auto-web take_screenshot --tab "$TAB"` |
| 断开 | `npx -y @zegocloud/auto-web disconnect` |
| 查看标签页 | `npx -y @zegocloud/auto-web list_tabs` |

说明：

- Web 当前没有 `assert` 命令。
- Web 的 `prompt` 必须同时包含操作和预期验证。
- 不要用 `grep` 匹配 `act` 输出判断通过；只看 exit code。

## Android: `@midscene/android@1`

来源：本地 `npx -y @midscene/android@1 --help`。

| 操作 | 命令 |
|------|------|
| 连接设备 | `npx -y @midscene/android@1 connect --device-id "$DEVICE_ID"` |
| 执行动作 | `npx -y @midscene/android@1 act --device-id "$DEVICE_ID" --prompt "$PROMPT"` |
| 断言 | `npx -y @midscene/android@1 assert --device-id "$DEVICE_ID" --prompt "$ASSERT_PROMPT"` |
| 截图 | `npx -y @midscene/android@1 take_screenshot --device-id "$DEVICE_ID"` |
| 断开 | `npx -y @midscene/android@1 disconnect` |

可选参数：

- `--use-scrcpy` / `--useScrcpy`
- `--device-id` 也可写作 `--deviceId`

## iOS: `@midscene/ios@1`

来源：本地 `npx -y @midscene/ios@1 --help`。

| 操作 | 命令 |
|------|------|
| 连接设备 | `npx -y @midscene/ios@1 connect --device-id "$DEVICE_ID"` |
| 执行动作 | `npx -y @midscene/ios@1 act --device-id "$DEVICE_ID" --prompt "$PROMPT"` |
| 断言 | `npx -y @midscene/ios@1 assert --device-id "$DEVICE_ID" --prompt "$ASSERT_PROMPT"` |
| 截图 | `npx -y @midscene/ios@1 take_screenshot --device-id "$DEVICE_ID"` |
| 断开 | `npx -y @midscene/ios@1 disconnect` |

可选参数：

- `--device-id` / `--deviceId`
- `--wda-host` / `--wdaHost`
- `--wda-port` / `--wdaPort`
- `--session-id` / `--sessionId`
- `--use-w-d-a` / `--useWDA`
- `--wda-mjpeg-port` / `--wdaMjpegPort`

## Desktop: `@midscene/computer@1`

| 操作 | 命令 |
|------|------|
| 连接桌面会话 | `npx -y @midscene/computer@1 connect` |
| 执行动作和验证 | `npx -y @midscene/computer@1 act --prompt "$PROMPT"` |
| 截图 | `npx -y @midscene/computer@1 take_screenshot` |
| 断开 | `npx -y @midscene/computer@1 disconnect` |

## HarmonyOS: `@midscene/harmony@1`

| 操作 | 命令 |
|------|------|
| 连接设备 | `npx -y @midscene/harmony@1 connect --deviceId "$DEVICE_ID"` |
| 执行动作和验证 | `npx -y @midscene/harmony@1 act --deviceId "$DEVICE_ID" --prompt "$PROMPT"` |
| 截图 | `npx -y @midscene/harmony@1 take_screenshot --deviceId "$DEVICE_ID"` |
| 断开 | `npx -y @midscene/harmony@1 disconnect` |

## 生成器使用原则

1. 平台差异由 `test-cases.json` 的 `runtime.platform` 和 `targets[].type` 表达。
2. `test-cases.sh` 由生成器选择命令，不由 agent 手写平台命令。
3. 当前项目特殊逻辑放到 `runtime.setupCommands`、`runtime.preConnectCommands`、`runtime.teardownCommands`。
4. 用例本身只能放在 `cases[]`，不能藏在 setup 或 teardown 里。
