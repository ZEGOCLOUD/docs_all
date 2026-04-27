---
name: zego-browser-automation
description: >
  Multi-tab web browser automation using @zegocloud/auto-web (powered by Midscene.js).
  Supports named tabs — multiple tabs can connect to the same URL for multi-user testing scenarios.

  Runs in headless Puppeteer — does NOT take over the user's mouse or keyboard.
  Browser and tab state persist across CLI invocations.

  Use this skill when the user wants to:
  - Test multi-user web applications (chat, collaboration, etc.)
  - Browse, navigate, or open web pages with named tabs
  - Fill out forms, click buttons, or interact with web elements
  - Verify, validate, test, or QA frontend UI behavior
  - Automate multi-step web workflows across multiple tabs
  - Take screenshots of specific tabs

  Trigger keywords: browser, web, multi-tab, multi-user, chat test, open browser,
  browse website, fill form, click button, screenshot web page, web automation,
  test web app, verify web UI, QA web, puppeteer

  Powered by @zegocloud/auto-web and Midscene.js (https://midscenejs.com)
allowed-tools:
  - Bash
---

# ZEGO Browser Automation (Multi-Tab)

> **CRITICAL RULES — VIOLATIONS WILL BREAK THE WORKFLOW:**
>
> 1. **Never run auto-web commands in the background.** Each command must run synchronously so you can read its output (especially screenshots) before deciding the next action. Background execution breaks the screenshot-analyze-act loop.
> 2. **Run only one auto-web command at a time.** Wait for the previous command to finish, read the screenshot, then decide the next action. Never chain multiple commands together.
> 3. **Allow enough time for each command to complete.** AI inference and screen interaction can take longer than typical shell commands. A typical command needs about 1 minute; complex `act` commands may need even longer.
> 4. **Always report task results before finishing.** After completing the automation task, you MUST proactively summarize the results to the user — including key data found, actions completed, screenshots taken, and any relevant findings. Never silently end after the last automation step; the user expects a complete response in a single interaction.
> 5. **Always specify --tab when multiple tabs are open.** When more than one tab exists, explicitly use `--tab <name>` on every command to avoid operating on the wrong tab.

Automate web browsing using `npx -y @zegocloud/auto-web`. Launches a headless Chrome via Puppeteer that **persists across CLI calls** — browser and tab state are preserved. Supports **named tabs** for multi-user testing scenarios (e.g., two users chatting on the same app).

## What `act` Can Do

Inside a single `act` call, Midscene can click, right-click, double-click, hover, type or clear text, press keys, scroll, drag, long-press, and continue through multi-step page flows based on what is currently visible.

## Prerequisites

Midscene requires models with strong visual grounding capabilities. The following environment variables must be configured — either as system environment variables or in a `.env` file in the current working directory:

```bash
MIDSCENE_MODEL_API_KEY="your-api-key"
MIDSCENE_MODEL_NAME="model-name"
MIDSCENE_MODEL_BASE_URL="https://..."
MIDSCENE_MODEL_FAMILY="family-identifier"
```

Example: Doubao Seed 2.0 Lite

```bash
MIDSCENE_MODEL_API_KEY="your-doubao-api-key"
MIDSCENE_MODEL_NAME="doubao-seed-2-0-lite"
MIDSCENE_MODEL_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
MIDSCENE_MODEL_FAMILY="doubao-seed"
```

If the model is not configured, ask the user to set it up. See [Model Configuration](https://midscenejs.com/model-common-config) for supported providers.

## Commands

### Connect a Named Tab

Every tab requires a unique name. Multiple tabs can point to the same URL.

```bash
npx -y @zegocloud/auto-web connect --url "https://example.com" --tab main
npx -y @zegocloud/auto-web connect --url "https://example.com" --tab user2
```

### List All Tabs

```bash
npx -y @zegocloud/auto-web list-tabs
```

### Take Screenshot

```bash
npx -y @zegocloud/auto-web take_screenshot --tab main
```

After taking a screenshot, read the saved image file to understand the current page state before deciding the next action.

### Perform Action

Use `act` to interact with the page. It autonomously handles all UI interactions internally — clicking, typing, scrolling, hovering, waiting, and navigating — so give it complex, high-level tasks as a whole. Describe **what you want to do and the desired effect** in natural language:

```bash
# --tab is required when multiple tabs exist
npx -y @zegocloud/auto-web act --tab main --prompt "fill in the email field with 'user@example.com' and click the Login button"

# --tab is optional when only one tab exists
npx -y @zegocloud/auto-web act --prompt "scroll down and click Submit"
```

### Element-Level Actions

All element-level actions support `--tab <name>`:

```bash
# Tap an element
npx -y @zegocloud/auto-web tap --tab main --locate '{"prompt": "the Submit button"}'

# Input text
npx -y @zegocloud/auto-web input --tab main --value "hello" --locate '{"prompt": "the search field"}'

# Scroll
npx -y @zegocloud/auto-web scroll --tab main --direction down

# Press a key
npx -y @zegocloud/auto-web keyboardpress --tab main --keyName "Enter"
```

### Close a Specific Tab

```bash
npx -y @zegocloud/auto-web close-tab --tab user2
```

### Close the Browser

```bash
npx -y @zegocloud/auto-web close
```

### Consume Report Files

The generated HTML report includes step-by-step execution details and replay videos for each operation.

```bash
npx -y @zegocloud/auto-web report-tool --action to-markdown --htmlPath ./midscene_run/report/.../index.html --outputDir ./output-markdown
```

## Workflow Patterns

### Single-Tab Workflow

1. **Connect** a tab: `connect --url <url> --tab main`
2. **Take screenshot** to verify the page loaded
3. **Execute actions** using `act`
4. **Close** when done: `close-tab --tab main`

### Multi-Tab Workflow (Multi-User Testing)

1. **Connect multiple tabs** (same or different URLs):
   ```bash
   auto-web connect --url "http://localhost:3000" --tab user1
   auto-web connect --url "http://localhost:3000" --tab user2
   ```
2. **Operate on each tab** with `--tab <name>`:
   ```bash
   auto-web act --tab user1 --prompt "login as Alice"
   auto-web act --tab user2 --prompt "login as Bob"
   auto-web act --tab user1 --prompt "send a message to Bob: Hello!"
   auto-web act --tab user2 --prompt "verify the message from Alice and reply Hi!"
   ```
3. **Verify** by taking screenshots of each tab
4. **Clean up**: `close-tab --tab user1` and `close-tab --tab user2`

## Best Practices

1. **Use meaningful tab names**: `user1`/`user2`, `admin`/`viewer`, `login`/`dashboard` — not generic names.
2. **Always specify --tab with multiple tabs**: Avoids accidentally operating on the wrong tab.
3. **Batch related operations into a single `act`**: "fill email, password, and click Login" as one command is faster than three separate commands.
4. **Be specific about UI elements**: Say `"the blue Submit button in the contact form"` instead of `"the button"`.
5. **Close tabs when done**: Use `close-tab` to free resources. Use `close` to shut down the entire browser.
6. **Never run in background**: Every auto-web command must run synchronously.
7. **Always report results after completion**: Summarize what was accomplished, present key data, and list generated files.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Chrome not found** | Install Google Chrome or set `MIDSCENE_MCP_CHROME_PATH`. |
| **API key error** | Check `.env` file or environment variables for `MIDSCENE_MODEL_API_KEY`. |
| **"Invalid combination of reasoning_effort"** | Unset `MIDSCENE_MODEL_REASONING_EFFORT`: `unset MIDSCENE_MODEL_REASONING_EFFORT` |
| **Tab not found** | Run `list-tabs` to see connected tabs. Re-connect with `connect --url --tab`. |
| **Command hangs** | The process should exit after each command. If it hangs, press Ctrl+C and retry. |
| **Screenshots not displaying** | The screenshot path is printed in the output. Use the Read tool to view it. |
