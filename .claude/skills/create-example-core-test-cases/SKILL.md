---
name: create-example-core-test-cases
description: >
  This skill should be used when the user asks to "create test cases", "write test cases for the example",
  "generate test cases", "design test cases for the demo", "create test-cases.md", "create test-cases.sh",
  or when the example-code-creator workflow reaches Step 8 (functional testing).
  Generates two files: test-cases.md (human-readable table) and test-cases.sh (automated Midscene test script).
  Focuses exclusively on core functionality — no edge cases, boundary testing, or non-core features.
---

# Create Example Core Test Cases

Generate test cases for ZEGO SDK example code projects. Output two files to the example project directory:

1. **`test-cases.md`** — Human-readable test case table for review
2. **`test-cases.sh`** — Executable bash script for automated Midscene testing

## Core Principle: Core-Only Coverage

This is **example code, not production software**. Test cases must cover only the **primary happy-path flows** that demonstrate the SDK's core capabilities. Skip:

- Empty input validation
- Duplicate entry prevention
- Logout/re-login flows
- Error message verification
- Navigation edge cases
- Boundary conditions
- Internationalization
- Data persistence across sessions

The goal is to verify that **the core feature works end-to-end**, not to QA-test the application.

## Workflow

### Step 1: Analyze the Example Code

Read and understand the example project's core functionality:

1. Read `{example_dir}/interaction-design.md` for the interaction flow
2. Read the main source files in `{example_dir}/src` to understand actual implementation
3. Identify the **core features** — typically 3-5 key capabilities the demo showcases
4. Determine the **user roles** needed (single user vs. multi-user)
5. Identify the **platform** (Web, Android, iOS, Desktop, HarmonyOS)

### Step 2: Design Core Test Cases

For each core feature, design **one test case** that validates the happy path. Follow these rules:

- **Multi-user scenarios**: If the feature involves interaction (chat, call, collaboration), design paired test cases — one for sender/actor, one for receiver/observer
- **Sequential flow**: Test cases should follow a natural user flow (login → action → verify)
- **Clear device assignment**: Each test case must specify which device/tab performs the action
- **Natural language**: Describe steps in precise, unambiguous natural language

**Typical test case count**: 5-10 cases for most examples. More than 10 suggests over-testing for an example project.

### Step 3: Generate test-cases.md

Write the test cases to `{example_dir}/test-cases.md` using this format:

```markdown
# Test Cases - {Project Name} ({Platform})

> Platform: {Platform} | Users: {N} ({user names}) | Core features only

## Test Cases

| TC# | Device/Tab | Test Case | Steps | Expected Result |
|-----|-----------|-----------|-------|-----------------|
| TC-01 | Tab: alice | Login - Alice | Enter User ID `user_alice`, click Login | Main page loads |
| TC-02 | Tab: bob | Login - Bob | Enter User ID `user_bob`, click Login | Main page loads |
| TC-03 | Tab: alice | Core Action | Description of steps | Expected outcome |
```

Column definitions:
- **TC#**: Sequential number with TC- prefix (TC-01, TC-02, ...)
- **Device/Tab**: The device ID or browser tab name (e.g., `Tab: alice`, `Device: device_alice`)
- **Test Case**: Short descriptive name
- **Steps**: Precise natural language description of what to do
- **Expected Result**: What should be visible/confirmed after the action

### Step 4: Generate test-cases.sh

Write the automated test script to `{example_dir}/test-cases.sh`. Select the correct platform template from **`references/platform-templates.md`**:

| Platform | Package | Connection | Act |
|----------|---------|------------|-----|
| Web | `@zegocloud/auto-web` | `npx -y @zegocloud/auto-web connect --url "$URL" --tab NAME` | `npx -y @zegocloud/auto-web act --tab NAME --prompt "..."` |
| Android | `@midscene/android@1` | `npx -y @midscene/android@1 connect --deviceId ID` | `npx -y @midscene/android@1 act --device-id ID --prompt "..."` |
| iOS | `@midscene/ios@1` | `npx -y @midscene/ios@1 connect` | `npx -y @midscene/ios@1 act --prompt "..."` |
| Desktop | `@midscene/computer@1` | `npx -y @midscene/computer@1 connect` | `npx -y @midscene/computer@1 act --prompt "..."` |
| HarmonyOS | `@midscene/harmony@1` | `npx -y @midscene/harmony@1 connect --deviceId ID` | `npx -y @midscene/harmony@1 act --deviceId ID --prompt "..."` |

#### Shell Script Guidelines

- **One `act` call per test case**: Each TC maps to one `act()` invocation
- **Descriptive prompts**: The `--prompt` text should be a complete, self-contained instruction including what to do and what to confirm
- **Result verification**: Use `grep -qi` on the act output with relevant keywords
- **Sleep between cross-user actions**: Add `sleep 3-5` when waiting for the other user/device to receive something
- **TOTAL_COUNT**: Set to the actual number of test cases
- **URL/Package**: Replace placeholder with the actual value from the example project

#### Prompt Writing Tips for act() Calls

The prompt passed to `act --prompt "..."` must be:
1. **Self-contained**: Include all context needed (no reference to previous steps)
2. **Action + verification**: "Do X, then confirm Y is visible"
3. **Specific**: Use exact element labels, button text, and field names from the UI
4. **Single purpose**: One test case = one core action to verify

Example prompt:
```
"Type 'Hello Bob!' in the message input field and press Enter. Confirm the message appears as a green bubble on the right."
```

### Step 5: Review with User

Present both files to the user for review:
1. Display the content of `test-cases.md`
2. Display the content of `test-cases.sh`
3. Ask if adjustments are needed

## Additional Resources

### Platform Templates (load only the one matching the example project)

- **`references/platform-web.md`** — Web (auto-web): single-user + multi-tab skeletons
- **`references/platform-android.md`** — Android (auto-android): single-device + multi-device skeletons
- **`references/platform-ios.md`** — iOS (auto-ios): single-device skeleton
- **`references/platform-desktop.md`** — Desktop (auto-desktop): single-session skeleton
- **`references/platform-harmonyos.md`** — HarmonyOS (auto-harmonyos): single-device skeleton

### Example Files

- **`examples/sample-test-cases.md`** — Example test cases for a ZIM chat demo showing the expected format and coverage scope
