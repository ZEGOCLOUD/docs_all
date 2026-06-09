# 示例：ZIM 简单聊天 - 核心测试用例

## test-cases.json 示例

以下是 ZIM 聊天 demo 的核心测试用例示例。注意只覆盖 **核心 happy-path 流程**，跳过空输入验证、重复联系人、消息持久化等边界场景。

```json
{
  "schemaVersion": "auto-test-demo/v1",
  "meta": {
    "product": "ZIM",
    "platform": "web",
    "scope": "simple-chat",
    "runName": "zim-web-simple-chat-2026-06-08",
    "demoName": "zim-web-simple-chat-demo",
    "projectDir": "doc-test-reports/zim-web-simple-chat-2026-06-08/examples/zim-web-simple-chat-demo",
    "reportDir": "doc-test-reports/zim-web-simple-chat-2026-06-08/auto-test"
  },
  "runtime": {
    "platform": "web",
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
      "label": "标签页: alice",
      "type": "web-tab",
      "tab": "alice",
      "url": "http://localhost:5173"
    },
    {
      "id": "bob",
      "label": "标签页: bob",
      "type": "web-tab",
      "tab": "bob",
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
      "action": "在用户 ID 输入框输入 user_alice，用户名输入 Alice，点击登录按钮",
      "expected": "页面跳转到主界面，显示聊天、联系人、我的标签，且没有报错信息",
      "screenshot": "TC-001-login-alice.png"
    },
    {
      "id": "TC-002",
      "title": "登录 - Bob",
      "target": "bob",
      "dependent": null,
      "precondition": "无",
      "action": "在用户 ID 输入框输入 user_bob，用户名输入 Bob，点击登录按钮",
      "expected": "页面跳转到主界面，显示聊天、联系人、我的标签，且没有报错信息",
      "screenshot": "TC-002-login-bob.png"
    },
    {
      "id": "TC-003",
      "title": "添加联系人",
      "target": "alice",
      "dependent": "TC-001",
      "precondition": "Alice 当前在主界面，且页面有已登录状态",
      "action": "切换到联系人标签，输入用户 ID user_bob，名称 Bob，点击添加",
      "expected": "Bob 出现在联系人列表中，且没有报错信息",
      "screenshot": "TC-003-add-contact.png"
    },
    {
      "id": "TC-004",
      "title": "发送消息",
      "target": "alice",
      "dependent": "TC-003",
      "precondition": "Alice 的联系人列表能看到联系人 Bob",
      "action": "点击联系人 Bob 打开聊天，输入“你好 Bob!”并按回车发送",
      "expected": "消息“你好 Bob!”显示在 Alice 侧消息列表中，且没有报错信息",
      "screenshot": "TC-004-send-message.png"
    },
    {
      "id": "TC-005",
      "title": "接收消息",
      "target": "bob",
      "dependent": ["TC-002", "TC-004"],
      "precondition": "Bob 当前在主界面，且页面有已登录状态",
      "action": "切换到聊天标签",
      "expected": "与 user_alice 的会话出现，最后一条消息为“你好 Bob!”，且没有报错信息",
      "screenshot": "TC-005-receive-message.png"
    },
    {
      "id": "TC-006",
      "title": "回复消息",
      "target": "bob",
      "dependent": "TC-005",
      "precondition": "Bob 的聊天列表中有来自 Alice 的消息“你好 Bob!”",
      "action": "打开与 Alice 的会话，输入“你好 Alice!”并按回车发送",
      "expected": "消息“你好 Alice!”显示在 Bob 侧消息列表中，且没有报错信息",
      "screenshot": "TC-006-reply-message.png"
    },
    {
      "id": "TC-007",
      "title": "接收回复",
      "target": "alice",
      "dependent": "TC-006",
      "precondition": "Alice 当前打开与 Bob 的聊天窗口，且已发送“你好 Bob!”",
      "action": "查看当前聊天窗口",
      "expected": "消息“你好 Alice!”显示在 Alice 侧消息列表中，且没有报错信息",
      "screenshot": "TC-007-receive-reply.png"
    }
  ]
}
```

## 设计要点

1. 7 个测试用例覆盖核心流程：登录 → 添加联系人 → 发送 → 接收 → 回复 → 接收。
2. 每个用例维护 `dependent`、`precondition`、`action`、`expected` 四段核心语义。
3. `dependent` 表达前置用例依赖；依赖用例未通过时，后续用例自动跳过。
4. 前提条件不满足时，用例直接失败，不继续执行操作。
5. 多用户流程用 `target` 明确区分 Alice 和 Bob。
6. 如果人工 review 后要调整用例，直接改 `test-cases.json`，再重新生成 `test-cases.sh`。
